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

    images_path = None
    dataset_path = None
    output_folder_path = None

    def __init__(self):
        pass

    '''
    Execution function
    '''
    def runner(self):
        choice = self.menu()

        if choice == 1:
            print('--------------------------------------Generating Dataset--------------------------------------')

            self.dataset_path = self.setFolderPath(subfolder='pdf', parent='PDF_To_Image')
            self.images_path = self.setFolderPath(subfolder='images', parent='PDF_To_Image')

            print('----------------------------------------Choosing File-----------------------------------------')
            # Use the file selection dialog to choose a file(s)
            bill_path = self.chooseFile()

            # Remove existing files in pdf folder and copy select files
            self.processSelectedFiles(bill_path)

            print('-----------------------------------Converting PDF to image------------------------------------')
            converter = PDFToImageConverter()
            converter.convertMultiplePdfs(self.dataset_path, self.images_path)

        elif choice == 2:
            self.output_folder_path = self.setFolderPath(subfolder='OCR_Output')
            print('----------------------------------------Choosing File-----------------------------------------')
            # Use the file selection dialog to choose a file(s)
            img_path = self.chooseFile()

            print('-----------------------------------Converting PDF to image------------------------------------')
            converter = PDFToImageConverter()
            converter.convertMultiplePdfs(self.dataset_path, self.images_path)


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
    def setFolderPath(subfolder, parent=None):
        if parent:
            folder_path = os.path.join(parent, subfolder)
        else:
            folder_path = f"/Images/{Path(subfolder).stem}_{str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))}"
            folder_path = os.getcwd() + folder_path

        try:
            os.makedirs(folder_path)
        except FileExistsError:
            pass

        return folder_path

    '''
    Select any files locally by popping up a window.
    @return path
    '''
    @staticmethod
    def chooseFile():
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
