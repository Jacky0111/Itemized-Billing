import os
import cv2

directory = 'TCD-yolo-1.1/obj_train_data/'

# Get all files in the directory
all_files = os.listdir(directory)

# Separate the files into two lists based on their format
txt_files = [file for file in all_files if file.endswith('.txt')]
jpg_files = [file for file in all_files if file.endswith('.jpg')]

# Iterate over the first item of the two lists together
for txt_file, jpg_file in zip(txt_files, jpg_files):
    file_path = os.path.join(directory, txt_file)

    # Read the image
    image = cv2.imread(directory + jpg_file)

    # Read values from the text file
    with open(directory + txt_file, 'r') as file:
        lines = file.readlines()

    # Process the lines and convert to a list of lists
    values = [list(map(float, line.strip().split()[1:])) for line in lines]

    # Convert format to xywh
    converted_values = []
    for value in values:
        x, y, w, h = value[0], value[1], value[2], value[3]
        x = int((x - w/2 + h/2) * image.shape[1])
        y = int((y + h/2) * image.shape[0])
        w = int(w * image.shape[1])
        h = int(h * image.shape[0])

        # Draw lines on the image
        cv2.line(image, (0, y), (image.shape[0]+w, y), (255, 0, 0), 2)
        cv2.line(image, (0, y-h), (image.shape[0]+w, y-h), (255, 0, 0), 2)

    # Display the image with lines
    cv2.imshow('Image with Lines', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    break

