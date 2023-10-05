import os
import cv2
import torch
import argparse
import numpy as np
from pathlib import Path

from ultralytics import YOLO
from ultralytics.utils import set_logging
from ultralytics.utils.ops import xyxy2xywh
from ultralytics.utils.torch_utils import select_device
from ultralytics.utils.plotting import Annotator, save_one_box


class Detect:
    """
    Execute trained weights to detect the table as well as annotate the Regions of Interest (ROI) of the image.
    @param opt
    @return img_saved_paths
    """
    @staticmethod
    def detect(opt):
        source = opt.source
        imgsz = opt.img_size
        weights = opt.weights
        save_txt = opt.save_txt

        # Directory information
        project = opt.project
        name = opt.name
        img_name = opt.img_name
        ext = opt.ext

        # Directories
        save_dir = Path(project) / name  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Initialize
        set_logging()
        device = select_device(opt.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = YOLO(weights)
        results = model.predict(source=source, save_txt=save_txt, imgsz=imgsz, half=half, conf=opt.conf_thres, save=True)

        # Get class name(s) from the YOLO model
        target_name = model.module.names if hasattr(model, 'module') else model.names

        # Load original image
        ori_img = cv2.imread(f'{save_dir}/{img_name}.{ext}')
        gn = torch.tensor(ori_img.shape)[[1, 0, 1, 0]]  # # Normalization gain whwh

        # Process the detection results
        result = results[0]
        cls = result.boxes.cls
        conf = result.boxes.conf

        xyxy = result.boxes.xyxy.to(device)  # Convert detected bounding boxes to the chosen device
        gn = gn.to(device)  # Move the normalization gain tensor to the chosen device
        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
        line = (cls, *xywh, conf) if opt.save_conf else (cls, xywh)  # label format

        if save_txt:
            with open(f'{save_dir}/bounding_box.txt', 'a') as f:
                # Write the first element of the tuple (tensor) as a float
                f.write('%g ' % line[0].item())  # Extract the float value from the tensor and write it

                # Write the second element of the tuple (list) as a series of floats
                for number in line[1]:
                    f.write('%g ' % number)  # Write each number followed by a space

                f.write('\n')  # Add a newline character at the end of the line

        # Save cropped image
        crop_img_name = f'{save_dir}/{img_name}_crop.png'
        save_one_box(xyxy, ori_img, file=Path(crop_img_name))

        # Save annotated image
        annotated_img_name = f'{save_dir}/{img_name}_annotated.png'
        label = f'{target_name[int(cls)]} {float(conf):.2f}'  # Text to display beside of the box
        xyxy = np.array(xyxy.tolist()).ravel()  # Flatten the numpy array
        annotator = Annotator(ori_img)
        annotator.box_label(xyxy, label, (0, 0, 255))  # Add one xyxy box to image with label
        annotated_img = annotator.result()  # Return annotated image as array
        cv2.imwrite(annotated_img_name, annotated_img)

    '''
    Define the required arguments to command-line interfaces.
    @param saved_path
    @param image_name
    '''
    @staticmethod
    def parseOpt(saved_path, image_name):
        parser = argparse.ArgumentParser()

        print(f'Saved path: {saved_path}')
        print(f'Image name: {image_name}')

        parser.add_argument('--weights', nargs='+', type=str, default='best.pt', help='model.pt path(s)')
        parser.add_argument('--source', type=str, default=saved_path, help='source')  # file/folder, 0 for webcam
        parser.add_argument('--img-size', type=int, default=416, help='inference size (pixels)')
        parser.add_argument('--conf-thres', type=float, default=0.8, help='object confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
        parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser.add_argument('--view-img', action='store_true', help='display results')
        parser.add_argument('--save-txt', action='store_true', default=True, help='save results to *.txt')
        parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
        parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
        parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
        parser.add_argument('--augment', action='store_true', help='augmented inference')
        parser.add_argument('--update', action='store_true', help='update all models')
        parser.add_argument('--project', default=os.path.split(saved_path)[0], help='save results to project/name')
        parser.add_argument('--name', default=os.path.split(saved_path)[1], help='save results to project/name')
        parser.add_argument('--img-name', default=image_name, help='image name in project/name')
        parser.add_argument('--ext', default='png', help='default image extension is *.png')
        parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        opt = parser.parse_args()
        print(opt)

        Detect.detect(opt)
