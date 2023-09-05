import os
import cv2
import time
import argparse
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
    def detect(opt, save_img=False):
        source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size

        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)

        # Directories
        save_dir = Path(opt.project) / opt.name  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Initialize
        set_logging()
        device = select_device(opt.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        device = select_device(opt.device)

        model = YOLO(weights)
        model.predict(source=source, weights=weights, view_img=view_img, save_txt=save_txt, imgsz=imgsz, half=half)

    '''
    Define the required arguments to command-line interfaces.
    @param saved_path
    @return img_saved_paths
    '''

    @staticmethod
    def parseOpt(saved_path):
        parser = argparse.ArgumentParser()

        print(f'Saved path: {saved_path}')

        parser.add_argument('--weights', nargs='+', type=str, default='best.pt', help='model.pt path(s)')
        parser.add_argument('--source', type=str, default=saved_path, help='source')  # file/folder, 0 for webcam
        parser.add_argument('--img-size', type=int, default=416, help='inference size (pixels)')
        parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
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
        parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        opt = parser.parse_args()
        print(opt)

        with torch.no_grad():
            if opt.update:  # update all models (to fix SourceChangeWarning)
                for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                    img_saved_paths = Detect.detect(opt)
                    strip_optimizer(opt.weights)
            else:
                img_saved_paths = Detect.detect(opt)

        return img_saved_paths
