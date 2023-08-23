import os
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate
from deskew import determine_skew


def deskew(input_path):
    image = io.imread(input_path)

    grayscale = rgb2gray(image)

    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    rotated = rotated.astype(np.uint8)

    io.imsave(input_path, rotated)


# input_image_path = 'HB-yolo-1.1/obj_train_data/BAGAN_001_aug3.png'
# output_image_path = 'output_deskewed.png'

directory = r'CVAT/Training Set'

# List all the image files in the folder
images = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Iterate through each image file and deskew
for index, img in enumerate(images):
    image_path = os.path.join(directory, img)
    print(f'{str(index+1)}. {image_path}')
    deskew(image_path)

# def deskew(_img):
#     image = io.imread(_img)
#     grayscale = rgb2gray(image)
#     angle = determine_skew(grayscale)
#     rotated = rotate(image, angle, resize=True) * 255
#     return rotated.astype(np.uint8)
#
#
# def display_avant_apres(_original):
#     plt.subplot(1, 2, 1)
#     plt.imshow(io.imread(_original))
#     deskewed_image = deskew(_original)
#     plt.subplot(1, 2, 2)
#     plt.imshow(deskewed_image)
#     plt.show()
#
#     # Save the deskewed image
#     output_path = 'output_deskewed.png'
#     io.imsave(output_path, deskewed_image)
