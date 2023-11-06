import os
import re
import io
import cv2
import numpy as np
import pandas as pd

from TabularRule import TabularRule

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCR:
    code = None
    header = None
    content = None
    output_path = None  # Current save path
    images_path = None  # Input images path
    is_non_native = False

    counter = 0
    df = pd.DataFrame()
    table_data_list = []
    data_coordinate_list = []

    def __init__(self, code, output_path, images_path):
        self.code = code
        self.output_path = output_path
        self.images_path = images_path

    '''
    Execution function
    '--oem 3' uses default LSTM OCR engine mode.
    '--psm 4' represents the Page Segmentation Mode and 4 assumes a single column of text.
    '''

    def runner(self):
        # Loop through all images
        for idx, file in enumerate(os.listdir(self.images_path)):
            # Construct the full path of the current image file
            img_path = os.path.join(self.images_path, file)
            img = cv2.imread(img_path)

            # Process the image using the imageToData method
            data, temp_df = self.imageToData(img, r'--oem 3 --psm 4 -l eng')
            temp_df = temp_df.loc[:, 'left':]

            # Additional step to check whether the header is correct detected
            if idx == 0:
                temp_df = self.checkHospital(temp_df)

            # Concatenate the data to the final DataFrame
            self.df = pd.concat([self.df, temp_df], ignore_index=True)

            # Draw bounding boxes on the image
            self.drawBoundingBox(img, data)
            cv2.imwrite(self.images_path + f'/bbox_{file}', img)

            # Store the bill in tabular format
            tr = TabularRule(temp_df, True if idx == 0 else False)
            tr.runner()
            self.table_data_list.append(tr.row_list)

        for i, ele in enumerate(self.table_data_list):
            print(f'{i}. {ele}')

        self.saveToCSV(self.df)

    '''
    Saved recognized text to json file
    @param path
    '''
    def saveToCSV(self, data):
        data.to_csv(f'{self.output_path}/image_to_data.csv', index=False)

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
        df = df.dropna()
        df = df.reset_index(drop=True)  # Reset the index
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

    def checkHospital(self, data):
        if self.code == 'BAGAN':
            return OCR.BAGANAdjustment(data)
        elif self.code == 'GNC':
            return OCR.GNCAdjustment(data)
        elif self.code == 'KPJ':
            return OCR.KPJAdjustment(data)
        elif self.code == 'RSH':
            return OCR.RSHAdjustment(data)

    @staticmethod
    def BAGANAdjustment(data):
        return

    @staticmethod
    def GNCAdjustment(data):
        return

    @staticmethod
    def KPJAdjustment(data):
        first_column = {'left': 0, 'top': data['top'][0], 'width': 0, 'height': 0, 'conf': 0, 'text': 'Item'}
        # Insert the new row at the beginning of the DataFrame
        data = pd.concat([pd.DataFrame(first_column, index=[0]), data]).reset_index(drop=True)

        return data

    @staticmethod
    def RSHAdjustment(data):
        return


