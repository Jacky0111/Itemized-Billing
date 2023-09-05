import cv2
import numpy as np


class DataPreprocessing:
    @staticmethod
    def adjustBrightness(img, brightness_factor):
        aug_image = img * brightness_factor
        return np.clip(aug_image, 0, 255).astype(np.uint8)

    @staticmethod
    def convertToGrayscale(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def resizeImage(img, width, height):
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    @staticmethod
    def applyGaussianBlur(img, kernel_size=(5, 5), sigma=0):
        return cv2.GaussianBlur(img, kernel_size, sigma)

    @staticmethod
    def applyMedianBlur(img, kernel_size=5):
        return cv2.medianBlur(img, kernel_size)

    @staticmethod
    def applyHistogramEqualization(img):
        return cv2.equalizeHist(img)

    @staticmethod
    def applyThresholding(img, threshold_value=128, max_value=255, threshold_type=cv2.THRESH_BINARY):
        _, thresholded_image = cv2.threshold(img, threshold_value, max_value, threshold_type)
        return thresholded_image

    @staticmethod
    def applyDilation(img, kernel_size=(5, 5), iterations=1):
        kernel = np.ones(kernel_size, np.uint8)
        return cv2.dilate(img, kernel, iterations=iterations)
