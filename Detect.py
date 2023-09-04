import os
import cv2
import time
import argparse
from numpy import random
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn


class Detect:
    """
    Define the required arguments to command-line interfaces.
    @param saved_path
    @return img_saved_paths
    """
    @staticmethod
    def parseOpt(saved_path):
        parser = argparse.ArgumentParser()

        print(f'Saved path: {saved_path}')

        parser.add_argument('--weights',
                            nargs='+',
                            type=str,
                            default='best.pt',
                            help='model.pt path(s)')
        parser.add_argument('--source', type=str,
                            default=saved_path,
                            help='source')  # file/folder, 0 for webcam
