import os
import cv2
import numpy as np

train_file = 'data/train.txt'

# Define your data directories
image_dir = 'train_data/images'
annotation_dir = 'train_data/annotations'
output_image_dir = 'augmented_data/images'
output_annotation_dir = 'augmented_data/annotations'


# Function to read image and bounding box annotations
def read_image_and_annotations(img_path, ann_path):
    img = cv2.imread(img_path)
    bboxes = []

    with open(ann_path, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            cid, xpoint, ypoint, width, height = map(float, line.strip().split())
            bboxes.append([cid, xpoint, ypoint, width, height])

    return img, bboxes


# Function to apply augmentation to an image and its bounding boxes
def apply_augmentation(img, bboxes):
    # Randomly apply rotation (between -10 to +10 degrees)
    angle = np.random.randint(-10, 11)
    height, width = img.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    augmented_image = cv2.warpAffine(img, rotation_matrix, (width, height))

    # Randomly apply horizontal flip (50% probability)
    if np.random.rand() > 0.5:
        augmented_image = cv2.flip(augmented_image, 1)
        for bbox in bboxes:
            bbox[1] = 1.0 - bbox[1]  # Adjust x-coordinate for flipped image

    # Randomly apply scaling (scale factor between 0.8 to 1.2)
    scale_factor = np.random.uniform(0.8, 1.2)
    scaled_width = int(width * scale_factor)
    scaled_height = int(height * scale_factor)
    augmented_image = cv2.resize(augmented_image, (scaled_width, scaled_height))
    scale_x = scaled_width / width
    scale_y = scaled_height / height
    for bbox in bboxes:
        bbox[1] *= scale_x
        bbox[2] *= scale_y
        bbox[3] *= scale_x
        bbox[4] *= scale_y

    return augmented_image, bboxes


# Data augmentation loop
for image_name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_name)
    annotation_name = image_name.replace(".png", ".txt")
    annotation_path = os.path.join(annotation_dir, annotation_name)

    print(f'image_name: {image_name}')
    print(f'image_path:{image_path}')
    print(f'annotation_name:{annotation_name}')
    print(f'annotation_path:{annotation_path}')

    image, bboxes = read_image_and_annotations(image_path, annotation_path)

    for i in range(5):  # Augment each image 5 times
        augmented_image, augmented_bboxes = apply_augmentation(image, bboxes)

        # Save the augmented image and annotations
        augmented_image_path = os.path.join(output_image_dir, f"{image_name[:-4]}_aug{i+1}.png")
        augmented_annotation_path = os.path.join(output_annotation_dir, f"{annotation_name[:-4]}_aug{i+1}.txt")

        cv2.imwrite(augmented_image_path, augmented_image)

        with open(augmented_annotation_path, "w") as file:
            for bbox in augmented_bboxes:
                class_id, x, y, w, h = bbox
                file.write(f"{class_id} {x} {y} {w} {h}\n")

# Get a list of all text file names in the input directory
text_file_names = [os.path.join('data/obj_train_data/', filename) for filename in os.listdir(output_annotation_dir) if filename.endswith('.txt')]

# Write the list of text file names to the "train.txt" file
with open(train_file, 'w') as f:
    for filename in text_file_names:
        f.write(filename + '\n')

print("File names written to train.txt")


