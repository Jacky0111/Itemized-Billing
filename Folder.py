import os


class Folder:
    @classmethod
    def getLastModifiedFolder(cls, directory):
        # Initialize variables to track the last modified folder and its timestamp
        last_modified_folder = None
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
                    last_modified_folder = folder

        return last_modified_folder


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
