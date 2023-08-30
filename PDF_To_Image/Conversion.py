import os
from pdf2image import convert_from_path


class PDFToImageConverter:
    # Set the path to the Poppler binary folder
    poppler_path = r'C:\poppler-23.01.0\Library\bin'
    os.environ["PATH"] += os.pathsep + poppler_path

    def __init__(self):
        pass

    def convertMultiplePdfs(self, input_folder, output_folder):
        pdf_files = [file for file in os.listdir(input_folder) if file.endswith('.pdf')]

        for pdf in pdf_files:
            path = os.path.join(input_folder, pdf)
            self.convertPdfToImages(path, output_folder)

    def convertPdfToImages(self, directory, output_folder, dpi=300):
        pdf_name = os.path.splitext(os.path.basename(directory))[0]
        output_folder_path = os.path.join(output_folder, pdf_name)
        os.makedirs(output_folder_path, exist_ok=True)

        print(f"Converting {pdf_name}.pdf to images...")
        images = convert_from_path(directory, dpi=dpi)

        self.saveImages(images, output_folder_path, pdf_name)

    @staticmethod
    def saveImages(images, output_folder, pdf_name):
        for idx, image in enumerate(images):
            img_path = os.path.join(output_folder, f'{pdf_name}_page_{idx + 1}.png')
            image.save(img_path, 'PNG')


if __name__ == "__main__":
    pdfs_folder = r'pdf'
    images_output_folder = r'images'

    converter = PDFToImageConverter()
    converter.convertMultiplePdfs(pdfs_folder, images_output_folder)
