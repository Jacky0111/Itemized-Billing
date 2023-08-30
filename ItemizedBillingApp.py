import os
import re
import wx
import shutil
import numpy as np

from pathlib import Path
from datetime import datetime

from PDF_To_Image.Conversion import PDFToImageConverter

class ItemizedBillingApp:
    data = []
    images = []  # To store the image converted from chosen invoice
    dataset_images = []  # To store the entire converted samples data
    invoice = None  # Chosen invoice
    img_counter = 0
    file_name = None
    folder_path = None

    images_path = None
    dataset_path = None

    def __init__(self):
        pass

    '''
    Execution function
    '''
    def runner(self):
        choice = self.menu()

        if choice == 1:
            print('--------------------------------------Generating Dataset--------------------------------------')
            self.dataset_path = self.setDatasetPath('pdf')
            self.images_path = self.setDatasetPath('images')

            # Use the file selection dialog to choose a file(s)
            bill_path = self.chooseFile()

            # Remove existing files in pdf folder and copy select files
            self.processSelectedFiles(bill_path)

            converter = PDFToImageConverter()
            converter.convertMultiplePdfs(self.dataset_path, self.images_path)


        elif choice == 2:
            print('----------------------------------------Choosing File-----------------------------------------')

    '''
    A main menu that allows user to choose either create a dataset or run ocr.
    @:return int
    '''
    @staticmethod
    def menu():
        print('MAIN MENU')
        print('=========')
        print('1. Create Dataset')
        print('2. Run OCR')
        return int(input('Enter your choice: '))

    '''
    Set the PDF and images folder path name
    '''
    @staticmethod
    def setDatasetPath(subfolder):
        folder_path = os.path.join(r'PDF_To_Image/', subfolder)
        try:
            os.makedirs(folder_path)
        except FileExistsError:
            pass

        return folder_path

    '''
    Select any files locally by popping up a window.
    @return path
    '''
    def chooseFile(self):
        app = wx.App(None)
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE | wx.DD_DIR_MUST_EXIST
        dialog = wx.FileDialog(None, 'Open', style=style)

        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()
        else:
            paths = []

        dialog.Destroy()

        return paths

    def processSelectedFiles(self, files):
        # Remove existing files in the destination folder
        for existing_file in os.listdir(self.dataset_path):
            file_path = os.path.join(self.dataset_path, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Copy the selected files to the destination folder
        for path in files:
            shutil.copy(path, self.dataset_path)


if __name__ == "__main__":
    ItemizedBillingApp().runner()
