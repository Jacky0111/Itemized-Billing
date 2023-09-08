import os
import re
import wx
import shutil
from pathlib import Path
from datetime import datetime

from Detect import Detect
from Conversion.Conversion import Converter


class ItemizedBillingApp:
    xml_path = None
    text_path = None
    images_path = None
    dataset_path = None
    output_folder_path = []

    def __init__(self):
        self.xml_path = None
        self.text_path = None
        self.images_path = None
        self.dataset_path = None
        self.output_folder_path.clear()

    '''
    Execution function
    '''
    def runner(self):
        choice = self.menu()

        if choice == 1:
            print('--------------------------------------Generating Dataset--------------------------------------')

            self.dataset_path = self.setFolderPath(subfolder='pdf', parent='Conversion')
            self.images_path = self.setFolderPath(subfolder='images', parent='Conversion')

            print('----------------------------------------Choosing File-----------------------------------------')
            # Use the file selection dialog to choose a file(s)
            bill_path = self.chooseFile()

            # Remove existing files in pdf folder and copy select files
            self.processSelectedFiles(bill_path, self.dataset_path)

            print('-----------------------------------Converting PDF to image------------------------------------')
            converter = Converter()
            converter.pdfToImages(self.dataset_path, self.images_path)

        elif choice == 2:
            print('--------------------------------------Generating Dataset--------------------------------------')
            self.text_path = self.setFolderPath(subfolder='text', parent='Conversion')
            self.xml_path = self.setFolderPath(subfolder='xml', parent='Conversion')

            print('----------------------------------------Choosing File-----------------------------------------')
            # Use the file selection dialog to choose a file(s)
            bill_path = self.chooseFile(allow_images=True)

            # Remove existing files in pdf folder and copy select files
            self.processSelectedFiles(bill_path, self.xml_path)

            print('------------------------------------Converting TXT to XML-------------------------------------')
            # converter = Converter()
            # converter.pdfToImages(self.dataset_path, self.images_path)

        elif choice == 3:
            print('----------------------------------------Choosing File-----------------------------------------')
            # Use the file selection dialog to choose a file(s)
            img_path = self.chooseFile()

            # Extract the pdf/img name from `img_path`
            img_name_list = [os.path.splitext(os.path.basename(path))[0] for path in img_path if path.lower()]
            subfolder = ['OCR_Output/' + name for name in img_name_list]

            self.output_folder_path = self.setFolderPath(subfolder=subfolder)

            # Copy the image from the source path to the destination path
            for source_path, dest_path in zip(img_path, self.output_folder_path):
                shutil.copy(source_path, dest_path)

            # print('-----------------------------------Converting PDF to image------------------------------------')
            # converter = PDFToImageConverter()
            # converter.convertMultiplePdfs(self.dataset_path, self.images_path)

            print('---------------------------------------Detecting Table----------------------------------------')
            for output_folder, img in zip(self.output_folder_path, img_name_list):
                Detect.parseOpt(output_folder, img)

            # print('-----------------------------------------Applying OCR-----------------------------------------')

    '''
    A main menu that allows user to choose either create a dataset or run ocr.
    @:return int
    '''
    @staticmethod
    def menu():
        print('MAIN MENU')
        print('=========')
        print('1. Create Dataset')
        print('2. Create XML file(s)')
        print('3. Run OCR')
        return int(input('Enter your choice: '))

    '''
    Set the PDF and images folder path name
    '''
    @staticmethod
    def setFolderPath(subfolder, parent=None):
        if parent:
            folder_path = os.path.join(parent, subfolder)
            ItemizedBillingApp.createFolder(folder_path)
        else:
            folder_path = []
            for folder in subfolder:
                path = f"{folder}_{str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))}"
                folder_path.append(path)
                ItemizedBillingApp.createFolder(path)

        return folder_path

    @staticmethod
    def createFolder(directory):
        try:
            os.makedirs(directory)
            print(f'{directory} has been made')
        except FileExistsError:
            pass

    '''
    Select any files locally by popping up a window.
    @return path
    '''
    @staticmethod
    def chooseFile(allow_images=False):
        app = wx.App(None)
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE | wx.DD_DIR_MUST_EXIST
        wildcard = "All files (*.*)|*.*"

        if allow_images:
            wildcard = "Image files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp|" + wildcard

        dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)

        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()
        else:
            paths = []

        dialog.Destroy()

        return paths

    @staticmethod
    def processSelectedFiles(files, destination):
        # Remove existing files in the destination folder
        for existing_file in os.listdir(destination):
            file_path = os.path.join(destination, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Copy the selected files to the destination folder
        for path in files:
            shutil.copy(path, destination)


if __name__ == "__main__":
    ItemizedBillingApp().runner()
