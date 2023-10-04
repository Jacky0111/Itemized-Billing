import os

folder_path = r'C:\Users\ChiaChungLim\PycharmProjects\Itemized-Billing\CVAT\KPJ'
new_prefix = 'KPJ_'

# Iterate over the files in the folder
for i, filename in enumerate(os.listdir(folder_path)):
    # Check if the file is a .png file (you can change the extension if needed)
    if filename.endswith('.png'):
        # Generate the new filename
        new_filename = f'{new_prefix}{i + 101}.png'

        # Create the full paths for the old and new filenames
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(old_path, new_path)
