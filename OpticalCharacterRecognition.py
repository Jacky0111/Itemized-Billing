import json
import os
import re
import io

import numpy as np
import pandas as pd

from cv2 import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCR:
    path = None  # Current save path
    image = None  # Input image
    header = None
    content = None
    is_non_native = False

    counter = 0

    data = dict()

    def __init__(self, path):
        self.data.clear()
        self.path = path

    '''
    Execution function
    @param img_path
    '''
    def runner(self, img_path):
        img = cv2.imread(img_path)
        data, df = self.imageToData(img, r'--oem 3 --psm 4 -l eng')
        df = df.loc[:, 'left':]
        self.drawBoundingBox(img, data)

        print(f'Current counter is {self.counter}')
        self.data, self.counter = self.header.runner(df, self.counter) if self.identifyClass(
            os.path.split(img_path)[1]) == 'head' \
            else self.content.runner(df, img, self.counter, self.path)
        print(f'Current counter is {self.counter}')
        self.saveToJson(self.path)