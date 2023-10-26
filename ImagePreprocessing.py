import cv2
import numpy as np


class ImagePreprocessing:
    """
    Convert the image to grayscale.
    """
    @staticmethod
    def Grayscale(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    '''
    Apply Gaussian blur to reduce noise and smooth the image.
    '''
    @staticmethod
    def GaussianBlur(img, kernel_size=(5, 5)):
        return cv2.GaussianBlur(img, kernel_size, 0)

    '''
    Apply adaptive thresholding to convert the image into a binary image.
    '''
    @staticmethod
    def Thresholding(img):
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    '''
    Apply morphological operations to further enhance the text in the image.
    '''
    @staticmethod
    def Morphological(img):
        kernel = np.ones((2, 2), np.uint8)
        return cv2.dilate(img, kernel, iterations=1)
