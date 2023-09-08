import os
import xml.etree.ElementTree as ET
from pdf2image import convert_from_path


class Converter:
    # Set the path to the Poppler binary folder
    poppler_path = r'C:\poppler-23.01.0\Library\bin'
    os.environ["PATH"] += os.pathsep + poppler_path

    def __init__(self):
        pass

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

    @staticmethod
    def txtToXml(input_folder, output_folder, cls, image_width, image_height):
        with open(input_folder, 'r') as file:
            lines = file.readlines()

        root = ET.Element("annotation")

        filename = ET.SubElement(root, "filename")
        filename.text = os.path.basename(input_folder).replace('.txt', '')

        size = ET.SubElement(root, "size")
        width = ET.SubElement(size, "width")
        height = ET.SubElement(size, "height")

        width.text = str(image_width)
        height.text = str(image_height)

        for line in lines:
            values = line.strip().split()
            if len(values) == 5:
                obj = ET.SubElement(root, "object")
                name = ET.SubElement(obj, "name")
                bbox = ET.SubElement(obj, "bndbox")
                xmin = ET.SubElement(bbox, "xmin")
                ymin = ET.SubElement(bbox, "ymin")
                xmax = ET.SubElement(bbox, "xmax")
                ymax = ET.SubElement(bbox, "ymax")

                class_index = int(values[0])
                class_name = cls[class_index]

                name.text = class_name
                xmin.text = str(int(float(values[1])))
                ymin.text = str(int(float(values[2])))
                xmax.text = str(int(float(values[3])))
                ymax.text = str(int(float(values[4])))

        tree = ET.ElementTree(root)
        tree.write(output_folder)

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
