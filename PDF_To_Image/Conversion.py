import os
from pdf2image import convert_from_path

# Set the path to the Poppler binary folder
poppler_path = r'C:\Program Files\poppler-23.05.0\Library\bin'
os.environ["PATH"] += os.pathsep + poppler_path


def convert_pdf_to_images(pdf_path, output_folder):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder_path = os.path.join(output_folder, pdf_name)
    os.makedirs(output_folder_path, exist_ok=True)

    print(f"Converting {pdf_name}.pdf to images...")
    images = convert_from_path(pdf_path, dpi=300)  # You can adjust the DPI as needed

    for idx, image in enumerate(images):
        img_path = os.path.join(output_folder_path, f'{pdf_name}_page_{idx + 1}.png')
        image.save(img_path, 'PNG')

    print(f"{pdf_name}.pdf has been successfully converted to images.")


if __name__ == "__main__":
    pdfs_folder = r'pdf'
    images_output_folder = r'images'

    pdf_files = [file for file in os.listdir(pdfs_folder) if file.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdfs_folder, pdf_file)
        convert_pdf_to_images(pdf_path, images_output_folder)
