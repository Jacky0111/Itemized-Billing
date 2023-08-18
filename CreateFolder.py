import os

dir_path = r'HB-yolo 1.1'
par_folder = r'obj_annotated_data'
folder_names = [f'{par_folder}/annotations', f'{par_folder}/images']

for folder_name in folder_names:
    folder_path = os.path.join(dir_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder '{folder_name}' created at '{dir_path}'")
