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
        source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
        # Directory variables
        project, name, img_name = opt.project, opt.name, opt.img_name

        # Directories
        save_dir = Path(opt.project) / opt.name  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Initialize
        set_logging()
        device = select_device(opt.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = YOLO(weights)
        results = model.predict(source=source, save_txt=save_txt, imgsz=imgsz, half=half, save=True)

        # Set Dataloader
        dataset = LoadImages(source, imgsz=imgsz)

        # Get names and colors
        target_name = model.module.names if hasattr(model, 'module') else model.names
        color = [[random.randint(0, 255) for _ in range(3)] for _ in target_name]

        # for data in dataset:
        #     iii = np.array(data[1])
        #     cv2.imshow('img', iii)
        #     cv2.waitKey(0)

            # for d in data:
            #     print(d)

        annotated_img_name = f'{save_dir}/{img_name}_annotated.png'
        crop_img_name = f'{save_dir}/{img_name}_crop.png'


        # Process results generator
        for result in results:
            boxes = result.boxes.data  # Boxes object for bbox outputs
            print(boxes)
        #     print(boxes.conf.tolist())
        #     # print(f'keypoints: {keypoints}')
        #     # print()
        #     # print(f'probs: {probs}')
        #     # print()


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
        parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        opt = parser.parse_args()
        print(opt)

        return Detect.detect(opt)
