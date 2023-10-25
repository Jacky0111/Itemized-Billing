import os
import re
import io
import cv2
import numpy as np
import pandas as pd

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCR:
    header = None
    content = None
    output_path = None  # Current save path
    images_path = None  # Input images path
    is_non_native = False

    counter = 0

    data = dict()

    def __init__(self, output_path, images_path):
        self.data.clear()
        self.output_path = output_path
        self.images_path = images_path

    '''
    Execution function
    '--oem 3' uses default LSTM OCR engine mode.
    '--psm 4' represents the Page Segmentation Mode and 4 assumes a single column of text.
    '''
    def runner(self):
        df1 = pd.DataFrame()

        # Loop through all images
        for file in os.listdir(self.images_path):
            # Construct the full path of the current image file
            img_path = os.path.join(self.images_path, file)
            img = cv2.imread(img_path)

            # Process the image using the imageToData method
            data, df2 = self.imageToData(img, r'--oem 3 --psm 4 -l eng')
            # df = df.loc[:, 'left':]

            # Concatenate the data to the final DataFrame
            df1 = pd.concat([df1, df2], ignore_index=True)

            # Draw bounding boxes on the image
            self.drawBoundingBox(img, data)

            cv2.imwrite(self.images_path + f'/bbox_{file}', img)
        self.saveToCSV(df1)

        # print(f'Current counter is {self.counter}')
        # self.data, self.counter = self.header.runner(df, self.counter) if self.identifyClass(
        #     os.path.split(img_path)[1]) == 'head' \
        #     else self.content.runner(df, img, self.counter, self.path)
        # print(f'Current counter is {self.counter}')
        # self.saveToCSV(df)

    '''
    Saved recognized text to json file
    @param path
    '''
    def saveToCSV(self, data):
        data.to_csv(f'{self.output_path}/data.csv', index=False)

    '''
    Perform image_to_data using pytesseract and store the data into DataFrame
    @param img
    @param config
    @return data, df
    '''
    @staticmethod
    def imageToData(img, config):
        data = pytesseract.image_to_data(img, config=config)
        s = io.StringIO(data)
        df = pd.read_csv(s, sep="\t")
        # df = df.dropna()
        # df.drop(df[(df.conf == 95)].index, inplace=True)
        return data, df

    '''
    Draw the bounding box based on the coordinate from pytesseract image to data
    @param img
    @param boxes
    '''
    @staticmethod
    def drawBoundingBox(img, boxes):
        red = (0, 0, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        for i, box in enumerate(boxes.splitlines()):
            if i == 0:
                continue

            box = box.split()

            if len(box) == 12:
                x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                cv2.rectangle(img, (x, y), (w + x, h + y), red, 1)
                cv2.putText(img, box[11] + ' ' + str(i), (x, y), font, 0.5, red, 1)

        # cv2.imwrite('bbox.png', img)

    '''
    Check whether the confidence scores of the image is high enough in order to determine native and non-native pdf
    @param df
    '''
    @staticmethod
    def checkConfidenceScore(df):
        df_conf = df.loc[(df['conf'] > 0) & (df['conf'] <= 70)]

        try:
            prob = df_conf.shape[0] / df.shape[0]
            print(f'{df_conf.shape[0]} / {df.shape[0]} = {prob}')
            return True if prob > 0.3 else False
        except ZeroDivisionError:
            print(f'{df_conf.shape[0]} / {df.shape[0]} = ALL PASS')

    '''
    Identify the object detected
    @param name
    @return cls
    '''
    @staticmethod
    def identifyClass(name):
        cls = None
        if re.search('head', os.path.split(name)[1]):
            cls = 'head'
        elif re.search('content', os.path.split(name)[1]):
            cls = 'content'
        return cls