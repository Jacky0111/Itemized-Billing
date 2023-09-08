import os
import shutil

# Define the source directory containing subfolders
source_directory = 'OCR_Output'

# Define the destination directory to copy "crop" images
destination_directory = 'Crop_Images'

# Iterate through subfolders in the source directory
for root, _, files in os.walk(source_directory):
    for filename in files:
        # Check if the filename contains "crop"
        if 'crop' in filename.lower() and filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            # Construct the source file path
            source_file_path = os.path.join(root, filename)

            # Construct the destination file path
            destination_file_path = os.path.join(destination_directory, filename)

            # Create the destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

            # Copy the file to the destination directory
            shutil.copy2(source_file_path, destination_file_path)

print("Image copying complete.")
