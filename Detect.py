import os
import cv2
import time
import argparse

import numpy as np
from numpy import random
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn

from ultralytics import YOLO
from ultralytics.utils import set_logging
from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors, save_one_box
from ultralytics.utils.ops import Profile, non_max_suppression, scale_coords, xyxy2xywh, scale_boxes
from ultralytics.data.loaders import LoadImages, LoadStreams, LoadScreenshots, IMG_FORMATS, VID_FORMATS
from ultralytics.utils.torch_utils import strip_optimizer, select_device, time_sync, smart_inference_mode
from ultralytics.utils.checks import check_imgsz, check_requirements, check_imshow, check_file, print_args


class Detect:
    """
    Execute trained weights to detect header and content as well as annotate the Regions of Interest (ROI) of the
    image.
    @param opt
    @param save_img
    @return img_saved_paths
    """
    @staticmethod
    def detect(opt):
        source, weights, save_txt, imgsz = opt.source, opt.weights, opt.save_txt, opt.img_size
        # Directory variables
        project, name, img_name, ext = opt.project, opt.name, opt.img_name, opt.ext

        # Directories
        save_dir = Path(opt.project) / opt.name  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Initialize
        set_logging()
        device = select_device(opt.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = YOLO(weights)
        results = model.predict(source=source, save_txt=save_txt, imgsz=imgsz, half=half, conf=opt.conf_thres, save=True)

        # Get names and colors
        target_name = model.module.names if hasattr(model, 'module') else model.names
        color = [[random.randint(0, 255) for _ in range(3)] for _ in target_name]

        ori_img = cv2.imread(f'{save_dir}/{img_name}.{ext}')
        gn = torch.tensor(ori_img.shape)[[1, 0, 1, 0]]  # normalization gain whwh

        for count, result in enumerate(results):
            print(f'xywh : {result.boxes.xywh}')

            xyxy = result.boxes.xyxy.to(device)
            gn = gn.to(device)
            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
            line = (result.boxes.cls, *xywh, result.boxes.conf) if opt.save_conf else (result.boxes.cls, xywh)  # label format
            print(f'xywh : {xywh}')
            print(f'line : {line}')

            with open(f'{save_dir}/line.txt', 'a') as f:
                # Write the first element of the tuple (tensor) as a float
                f.write('%g ' % line[0].item())  # Extract the float value from the tensor and write it

                # Write the second element of the tuple (list) as a series of floats
                for number in line[1]:
                    f.write('%g ' % number)  # Write each number followed by a space

                f.write('\n')  # Add a newline character at the end of the line

            annotated_img_name = f'{save_dir}/{img_name}_annotated.png'
            crop_img_name = f'{save_dir}/{img_name}_crop.png'
            label = f'{target_name[int(result.boxes.cls)]} {float(result.boxes.conf):.2f}'
            # plot_one_box(xyxy, ori_img, label=label, color=colors[int(result.boxes.cls)], line_thickness=3)

            save_one_box(xyxy, ori_img, file=Path(crop_img_name))

            print(f'xyxy[0]: {xyxy[0]}')
            print(f'xyxy[1]: {xyxy[1]}')

            x1 = int(xyxy.tolist()[0])
            y1 = int(xyxy.tolist()[1])
            x2 = int(xyxy.tolist()[2])
            y2 = int(xyxy.tolist()[3])

            annotated_img = cv2.rectangle(ori_img, (x1, y1), (x2, y2), color=color, thickness=2)
            annotated_img = cv2.putText(annotated_img, label, (x1, y1), color=color, thickness=2)
            cv2.imwrite(annotated_img_name, annotated_img)

            # print(f'keypoints: {keypoints}')
            # print()
            # print(f'probs: {probs}')
            # print()


        # # Set Dataloader
        # dataset = LoadImages(source, imgsz=imgsz)
        #

        #

        #
        # # Process results generator

        img_saved_paths = []

        return img_saved_paths

    '''
    Define the required arguments to command-line interfaces.
    @param saved_path
    @return img_saved_paths
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
        parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
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

        return Detect.detect(opt)
