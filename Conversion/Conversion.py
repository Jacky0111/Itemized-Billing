# Facilitates the PDF to image conversion functionality


import os
from pdf2image import convert_from_path


class Converter:
    # Set the path to the Poppler binary folder
    poppler_path = r'C:\poppler-23.01.0\Library\bin'
    os.environ["PATH"] += os.pathsep + poppler_path

    def __init__(self):
        pass

    '''
    Convert PDF files to images.
    @param input_folder: A string representing the path to the folder containing PDF files.
    @param output_folder: A string representing the path to the folder where the converted images will be saved.
    '''
    @staticmethod
    def pdfToImages(input_folder, output_folder):
        pdf_files = [file for file in os.listdir(input_folder) if file.endswith('.pdf')]

        for pdf in pdf_files:
            path = os.path.join(input_folder, pdf)

            pdf_name = os.path.splitext(os.path.basename(path))[0]
            output_folder_path = os.path.join(output_folder, pdf_name)
            os.makedirs(output_folder_path, exist_ok=True)

            print(f"Converting {pdf_name}.pdf to images...")
            images = convert_from_path(path, dpi=300)

            Converter.saveImages(images, output_folder_path, pdf_name)

    '''
    Save converted images to the output folder.
    @param images: A list of images to be saved.
    @param output_folder: A string representing the path to the folder where the images will be saved.
    @param pdf_name: A string representing the name of the original PDF file (without extension).
    '''
    @staticmethod
    def saveImages(images, output_folder, pdf_name):
        for idx, image in enumerate(images):
            img_path = os.path.join(output_folder, f'{pdf_name}_page_{idx + 1}.png')
            image.save(img_path, 'PNG')


if __name__ == "__main__":
    pdfs_folder = r'pdf'
    images_output_folder = r'images'

    converter = Converter()
    converter.pdfToImages(pdfs_folder, images_output_folder)
