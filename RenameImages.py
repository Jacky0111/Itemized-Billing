import os


class Rename:
    def __init__(self, folder_path, prefix='KPJ_'):
        self.folder_path = folder_path
        self.prefix = prefix

    def scenario1(self):
        # Iterate over the files in the folder
        for i, filename in enumerate(os.listdir(self.folder_path)):
            # Check if the file is a .png file (you can change the extension if needed)
            if filename.endswith('.png'):
                # Generate the new filename
                new_filename = f'{self.prefix}{i + 101}.png'

                # Create the full paths for the old and new filenames
                old_path = os.path.join(self.folder_path, filename)
                new_path = os.path.join(self.folder_path, new_filename)

                # Rename the file
                os.rename(old_path, new_path)

    def scenario2(self):
        allowed_extensions = ['.png', '.jpg', '.jpeg']  # Add more extensions as needed

        # Iterate over the files in the folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has an allowed image extension
            if any(filename.endswith(ext) for ext in allowed_extensions) and 'crop' in filename:
                # Remove the last 4 characters from the filename (excluding the extension)
                base_filename, file_extension = os.path.splitext(filename)
                new_filename = f'{base_filename[:-5]}{file_extension}'

                # Create the full paths for the old and new filenames
                old_path = os.path.join(self.folder_path, filename)
                new_path = os.path.join(self.folder_path, new_filename)

                # Rename the file
                os.rename(old_path, new_path)


if __name__ == "__main__":
    # folder_path = r'C:\Users\ChiaChungLim\PycharmProjects\Itemized-Billing\CVAT\KPJ'
    folder_path = r'C:\Users\CP1\Documents\GitHub\Itemized-Billing\Crop_Images'
    new_prefix = 'KPJ_'

    renamer = Rename(folder_path, new_prefix)

    # To execute scenario1:
    # renamer.scenario1()

    # To execute scenario2:
    renamer.scenario2()
