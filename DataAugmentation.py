import os
import cv2
import numpy as np


'''
Read image and bounding box annotations from files.
@:param img_path (str): Path to the image file.
@:param ann_path (str): Path to the annotation file.
@:return tuple: A tuple containing the following elements:
            - img (numpy.ndarray): The image read using OpenCV.
            - bboxes (list): A list of bounding box annotations, where each annotation is a list [cid, xpoint, ypoint, width, height].
'''
def ReadImageAndAnnotations(img_path, ann_path):
    img = cv2.imread(img_path)

    bboxes = []

    with open(ann_path, "r") as fp:
        lines = fp.readlines()

        for line in lines:
            # Split the line into individual values and convert them to floats
            cid, xpoint, ypoint, width, height = map(float, line.strip().split())
            bboxes.append([cid, xpoint, ypoint, width, height])

    # Return the image and the list of bounding box annotations as a tuple
    return img, bboxes

'''
Apply rotation to an image.
@:param img (numpy.ndarray): The input image.
@:param angle (int): The rotation angle in degrees.
@:return numpy.ndarray: The rotated image.
'''
def applyRotation(img, angle):
    height, width = img.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    aug_image = cv2.warpAffine(img, rotation_matrix, (width, height))
    return aug_image

'''
Apply scaling to an image.
@:param img (numpy.ndarray): The input image.
@:param scale_factor (float): The scaling factor.
@:return numpy.ndarray: The scaled image.
'''
def applyScaling(img, scale_factor):
    scaled_width = int(img.shape[1] * scale_factor)
    scaled_height = int(img.shape[0] * scale_factor)
    aug_image = cv2.resize(img, (scaled_width, scaled_height))
    return aug_image

'''
Adjust the brightness of an image.
@:param img (numpy.ndarray): The input image.
@:param brightness_factor (float): The brightness adjustment factor.
@:return numpy.ndarray: The adjusted image.
'''
def adjustBrightness(img, brightness_factor):
    aug_image = img * brightness_factor
    aug_image = np.clip(aug_image, 0, 255).astype(np.uint8)
    return aug_image

'''
Apply various augmentations to an image and its bounding boxes.
@:param img (numpy.ndarray): The input image.
@:param bboxes (list): List of bounding boxes, where each bounding box is represented as [class, x_min, y_min, x_max, y_max].
@:return tuple: A tuple containing the augmented image (numpy.ndarray) and the updated bounding boxes (list).
'''
def applyAugmentation(img, bboxes):
    # Randomly apply rotation (between -10 to +10 degrees)
    angle = np.random.randint(-10, 11)
    aug_image = applyRotation(img, angle)

    # Randomly apply scaling (scale factor between 0.8 to 1.2)
    scale_factor = np.random.uniform(0.8, 1.2)
    aug_image = applyScaling(aug_image, scale_factor)
    scale_x = aug_image.shape[1] / img.shape[1]
    scale_y = aug_image.shape[0] / img.shape[0]

    for bbox in bboxes:
        bbox[1] *= scale_x
        bbox[2] *= scale_y
        bbox[3] *= scale_x
        bbox[4] *= scale_y

    # Randomly adjust brightness (change brightness by up to 30%)
    brightness_factor = 1 + np.random.uniform(-0.3, 0.3)
    aug_image = adjustBrightness(aug_image, brightness_factor)

    return aug_image, bboxes

'''
Read an image and its associated annotations.
@:param image_path (str): The path to the image file.
@:param annotation_path (str): The path to the annotations file.
@:return tuple: A tuple containing the image (numpy.ndarray) and a list of bounding boxes (list).
'''
def readImgAndAnnotations(image_path, annotation_path):
    image = cv2.imread(image_path)

    # Parse bounding box annotations from the text file
    bboxes = []
    with open(annotation_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 5:
                class_id, x, y, w, h = map(float, values)
                bboxes.append([class_id, x, y, w, h])

    return image, bboxes

'''
Save augmented data (image and annotations) to the output directory.
@:param image (numpy.ndarray): The augmented image.
@:param augmented_bboxes (list): List of augmented bounding boxes.
@:param output_dir (str): The directory to save the augmented data.
@:param image_name (str): The name of the original image.
@:param annotation_name (str): The name of the original annotations file.
'''
def saveAugmentedData(image, augmented_bboxes, output_dir, image_name, annotation_name):
    for i in range(5):  # Augment each image 5 times
        augmented_image_path = os.path.join(output_dir, f"{image_name[:-4]}_aug{i + 1}.png")
        augmented_annotation_path = os.path.join(output_dir, f"{annotation_name[:-4]}_aug{i + 1}.txt")

        # Save the augmented image
        cv2.imwrite(augmented_image_path, image)

        # Save the augmented bounding box annotations
        with open(augmented_annotation_path, "w") as file:
            for bbox in augmented_bboxes:
                class_id, x, y, w, h = bbox
                file.write(f"{class_id} {x} {y} {w} {h}\n")


def main():
    # Define your data directories
    image_dir = 'HB-yolo-1.1/obj_annotated_data/images'
    annotation_dir = 'HB-yolo-1.1/obj_annotated_data/annotations'
    output_dir = 'HB-yolo-1.1/obj_train_data/'
    train_file = r'HB-yolo-1.1/train.txt'

    # Data augmentation loop
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        annotation_name = image_name.replace(".png", ".txt")
        annotation_path = os.path.join(annotation_dir, annotation_name)

        print(f'image_name: {image_name}')
        print(f'image_path: {image_path}')
        print(f'annotation_name: {annotation_name}')
        print(f'annotation_path: {annotation_path}')

        image, bboxes = readImgAndAnnotations(image_path, annotation_path)

        for i in range(5):  # Augment each image 5 times
            augmented_image, augmented_bboxes = applyAugmentation(image, bboxes)

            # Save the augmented image and annotations
            saveAugmentedData(
                augmented_image, augmented_bboxes, output_dir, image_name, annotation_name
            )

    # Get a list of all text file names in the input directory
    text_file_names = [
        os.path.join(output_dir, filename)
        for filename in os.listdir(output_dir)
        if filename.endswith('.png')
    ]

    # Write the list of text file names to the "train.txt" file
    with open(train_file, 'w') as f:
        for filename in text_file_names:
            f.write(filename + '\n')

    print("File names written to train.txt")


if __name__ == "__main__":
    main()
