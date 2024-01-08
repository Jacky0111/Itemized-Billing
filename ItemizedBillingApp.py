# Empowers the end user to make choices between performing document conversion and optical character recognition (OCR)


import os
import wx
import cv2
import shutil
from datetime import datetime

from Detect import Detect
from Conversion.Conversion import Converter
from OpticalCharacterRecognition import OCR


class ItemizedBillingApp:
    images_path = None
    dataset_path = None
    output_folder_path = []

    def __init__(self):
        self.images_path = None
        self.dataset_path = None
        self.output_folder_path.clear()

    '''
    Execution function
    '''
    def runner(self):
        choice = self.mainMenu()

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
            sub_choice = self.subMenu()

            hospital_code = None
            if sub_choice == 1:
                hospital_code = 'BAGAN'
            elif sub_choice == 2:
                hospital_code = 'GNC'
            elif sub_choice == 3:
                hospital_code = 'KPJ'
            elif sub_choice == 4:
                hospital_code = 'RSH'

            print('----------------------------------------Choosing File-----------------------------------------')
            # Use the file selection dialog to choose a file(s)
            img_path = self.chooseFile(True, hospital_code)

            # Extract the pdf/img name from `img_path`
            img_list = [os.path.splitext(os.path.basename(path))[0] for path in img_path if path.lower()]
            subfolder = ['OCR_Output/' + name for name in img_list]

            self.output_folder_path = self.setFolderPath(subfolder=subfolder)

            # Copy the image from the source path to the destination path
            for source_path, dest_path in zip(img_path, self.output_folder_path):
                shutil.copy(source_path, dest_path)

            print('---------------------------------------Detecting Table----------------------------------------')
            for output_folder, img in zip(self.output_folder_path, img_list):
                Detect.parseOpt(output_folder, img, 'table.pt', 0.8)

            print('----------------------------------------Detecting Row-----------------------------------------')
            # Create a list of modified image names
            new_img_list = [name + '_crop' for name in img_list]

            for output_folder, img in zip(self.output_folder_path, new_img_list):
                # Utilize the 'parseOpt' method to detect rows using the 'row.pt' file and a threshold of 0.4
                Detect.parseOpt(output_folder, img, 'row.pt', 0.3)

                # Define paths for the table image and row boxes
                table_img_path = f'{output_folder}/{img}.png'
                row_boxes_path = f'{output_folder}/labels/row_boxes.txt'

                # Read the table image
                tb_img = cv2.imread(table_img_path)
                crop_img = tb_img.copy()

                # Read values from the row boxes text file
                with open(row_boxes_path, 'r') as file:
                    lines = file.readlines()
                    # Remove the first value of the line and convert them to a nested list
                    values = [list(map(float, line.strip().split()[1:])) for line in lines]
                    # Sort based on the third value (y) in ascending order
                    values.sort(key=lambda j: j[1], reverse=False)

                # Update the text file with the sorted values
                with open(row_boxes_path, 'w') as file:
                    for value in values:
                        file.write(f'0 {value[0]} {value[1]} {value[2]} {value[3]}\n')

                # Create "Row" folder
                os.makedirs(os.path.join(output_folder, 'Row'), exist_ok=True)
                row_folder = f'{output_folder}/Row'

                # Convert the format to xywh and draw lines on the image
                for idx, value in enumerate(values):
                    x, y, w, h = value[0], value[1], value[2], value[3]
                    y = int((y + h / 2) * tb_img.shape[0])
                    w = int(w * tb_img.shape[1])
                    h = int(h * tb_img.shape[0])

                    # Draw lines on the image
                    cv2.line(tb_img, (0, y), (tb_img.shape[0] + w, y), (255, 0, 0), 2)
                    cv2.line(tb_img, (0, y - h), (tb_img.shape[0] + w, y - h), (255, 0, 0), 2)

                    # Crop the row based on the coordinates
                    cropped_row = crop_img[y - h:y, 0:crop_img.shape[1]]

                    # Save the cropped row in the 'Row' folder
                    cv2.imwrite(f'{row_folder}/row_{str(idx).zfill(3)}.png', cropped_row)

                # Save the annotated image
                cv2.imwrite(f'{output_folder}/{img[:-5]}_row_revised.png', tb_img)

                print('-----------------------------------------Applying OCR-----------------------------------------')
                ocr = OCR(hospital_code, output_folder, row_folder)
                ocr.runner()

                print('---------------------------------------------End----------------------------------------------')

    '''
    A main menu that allows user to choose either create a dataset or run ocr.
    @return int: User's choice
    '''
    @staticmethod
    def mainMenu():
        print('MAIN MENU')
        print('=========')
        print('1. Create Dataset')
        print('2. Run OCR')
        return int(input('Enter your choice: '))

    '''
    A main menu that allows user to choose either create a dataset or run ocr.
    @return int: User's choice
    '''
    @staticmethod
    def subMenu():
        print('\nHospital MENU')
        print('=============')
        print('1. BAGAN Specialist Center')
        print('2. Gleneagles')
        print('3. KPJ Healthcare')
        print('4. Regency Specialist Center')
        return int(input('Enter your hospital: '))

    '''
    Set the PDF and images folder path name.
    @param subfolder: a string/list of strings representing the name of the subfolder(s) are to be created.
    @param parent: a string representing the name of the parent folder. Default is None.
    @return folder_path: string or list of strings representing the created folder paths.
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

    '''
    Create a new folder if it does not already exist.
    @param directory: a string representing the path of the directory to be created.
    '''
    @staticmethod
    def createFolder(directory):
        try:
            os.makedirs(directory)
            print(f'{directory} has been made')
        except FileExistsError:
            pass

    '''
    Select any files locally by popping up a window.
    @param allow_images: a boolean indicating whether to allow only image files or all files. Default is False.
    @return paths: a list of strings representing the selected file paths.
    '''
    @staticmethod
    def chooseFile(allow_images=False, code=None):
        # Initializes a wxPython application
        app = wx.App(None)
        # Specifies the style for the file dialog, ensuring that the user can only select existing files
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE | wx.DD_DIR_MUST_EXIST
        wildcard = "All files|*.*"

        if allow_images:
            wildcard = "Image files|*.png;*.jpg;*.jpeg;*.bmp|" + wildcard

        if code:
            all_files = [f for f in os.listdir('CVAT/Training Set') if code in f]
            if all_files:
                wildcard = f"KPJ files|{';'.join(all_files)}|" + wildcard

        # Creates a file dialog window with the specified title and style.
        dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)

        # Checks if the user has selected a file in the file dialog
        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()  # Retrieves the path of the selected file
        else:
            paths = []

        dialog.Destroy()  # Destroys the file dialog window.

        return paths

    '''
    Process the selected files by copying them to the specified destination folder.
    @param files: a list of strings representing the paths of the files to be processed.
    @param destination: a string representing the path of the destination folder.
    '''
    @staticmethod
    def processSelectedFiles(files, destination):
        # Remove existing files in the destination folder
        for existing_file in os.listdir(destination):
            file_path = os.path.join(destination, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove the existing file

        # Copy the selected files to the destination folder
        for path in files:
            shutil.copy(path, destination)  # Copy the file to the destination folder


if __name__ == "__main__":
    ItemizedBillingApp().runner()
