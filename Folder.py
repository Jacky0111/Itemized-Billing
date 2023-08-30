import os


class Folder:
    """
    Get the name of the most recently modified folder in a directory.
    @:param directory (str): The path to the directory to search for folders.
    @:return latest_folder (str or None): The name of the most recently modified folder within the specified directory,
                                          or None if no folders are found.
    """
    @classmethod
    def getLastModifiedFolder(cls, directory):
        # Initialize variables to track the last modified folder and its timestamp
        latest_folder = None
        last_modified_timestamp = 0

        # Iterate through the directories in the specified directory
        for folder in os.listdir(directory):
            folder_path = os.path.join(directory, folder)

            # Check if it's a directory
            if os.path.isdir(folder_path):
                # Get the modification timestamp of the directory
                folder_timestamp = os.path.getmtime(folder_path)

                # Compare timestamps to find the most recent folder
                if folder_timestamp > last_modified_timestamp:
                    last_modified_timestamp = folder_timestamp
                    latest_folder = folder

        return latest_folder

    '''
    Create folders under a specified directory path.
    @:param dir_path (str): The base directory path where folders will be created.
    @:param parent_folder (str): The name of the parent folder under which sub-folders will be created.
    @:param folder_names (list): A list of folder names to create as sub-folders of the parent folder.
    '''
    @staticmethod
    def createFolders(dir_path, parent_folder, folder_names):
        for folder_name in folder_names:
            folder_path = os.path.join(dir_path, parent_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder_name}' created at '{dir_path}'")


if __name__ == "__main__":
    # Specify the directory you want to search in
    directory_to_search = '/path/to/your/directory'

    # Get the last modified folder
    last_modified_folder = Folder.getLastModifiedFolder(directory_to_search)

    if last_modified_folder:
        print("Last Modified Folder:", last_modified_folder)
        print("Timestamp:", os.path.getmtime(os.path.join(directory_to_search, last_modified_folder)))
    else:
        print("No folders found in the directory.")
