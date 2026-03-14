import os
# Define the path (override with RENAME_DIR to improve portability)
path = os.environ.get("RENAME_DIR", r"C:\Users\ChiaChungLim\PycharmProjects\Consignment-Itemized-Data\data\KPJ_01")
# Change directory
os.chdir(path)
# List all files in the directory
files = os.listdir()
# Filter out directories (if any)
files = [f for f in files if os.path.isfile(f)]
# Sort files based on their names
files.sort()
# Define a counter for renaming
counter = 1
# Rename files
for file_name in files:
    # Split the file name and extension
    name, ext = os.path.splitext(file_name)
    # Generate new file name with format KPJ_001, KPJ_002, ...
    new_name = f"KPJ_{counter:03}{ext}"
    # Rename the file
    os.rename(file_name, new_name)
    # Increment counter
    counter += 1
print("Files renamed successfully.")
