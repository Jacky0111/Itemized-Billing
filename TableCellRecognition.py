import os
import cv2
import numpy as np
from imutils import resize


class TabelCellRecognition:
    directory = None

    def __init__(self, directory):
        self.directory = directory

    def processor(self):
        # Check if the specified directory exists
        if not os.path.exists(self.directory):
            print(f"Directory '{self.directory}' does not exist.")
            return

        # Get a list of image files in the directory
        images = [f for f in os.listdir(self.directory) if f.endswith(('.jpg', '.jpeg', '.png'))]

        if not images:
            print(f"No image files found in '{self.directory}'.")
            return

        for i, img in enumerate(images):
            # Construct the full path to the image file
            image_path = os.path.join(self.directory, img)

            # Read the image using OpenCV
            img = cv2.imread(image_path)

            if img is not None:
                # Get the width and height of the image
                height, width, _ = img.shape

                # Print or process the width and height as needed
                print(f"Width: {width}, Height: {height}")
            else:
                print(f"Failed to read image: {img}")

            # threshold and resize table image
            tbl_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            tbl_thresh_bin = cv2.threshold(tbl_gray, 127, 255, cv2.THRESH_BINARY)[1]

            R = 2.5
            tbl_resized = resize(tbl_thresh_bin, width=int(img.shape[1] // R))

            dims = img.shape[0], img.shape[1]

            # table mask to search for gridlines
            tbl_str = np.zeros(dims, np.uint8)
            tbl_str = cv2.rectangle(tbl_str, (0, 0), (dims[1] - 1, dims[0] - 1), 255, 1)

            for a in [0, 1]:
                dividers = TabelCellRecognition.getDividers(tbl_resized, a)
                start_point = [0, 0]
                end_point = [dims[1], dims[1]]
                for i in dividers:
                    i *= R
                    start_point[a] = int(i)
                    end_point[a] = int(i)
                    cv2.line(tbl_str,
                             tuple(start_point),
                             tuple(end_point),
                             255,
                             1)

            contours, hierarchy = cv2.findContours(tbl_str, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours, boundingBoxes = TabelCellRecognition.sortContours(contours, method='top-to-bottom')

            # remove countours of the whole table
            bb_filtered = [list(t) for t in boundingBoxes
                           if t[2] < dims[1] and t[3] < dims[0]]

            # allocate countours in table-like structure
            rows = []
            columns = []

            for i, bb in enumerate(bb_filtered):
                if i == 0:
                    columns.append(bb)
                    previous = bb
                else:
                    if bb[1] < previous[1] + previous[3] / 2:
                        columns.append(bb)
                        previous = bb
                        if i == len(bb_filtered) - 1:
                            rows.append(columns)
                    else:
                        rows.append(columns)
                        columns = []
                        previous = bb
                        columns.append(bb)

                    cv2.rectangle(img, (bb[0], bb[1]), (bb[0] + bb[2], bb[1] + bb[3]), (0, 255, 0), 2)

            cv2.imwrite(f'annotated_table_{i + 1}.jpg', img)

    @staticmethod
    def getDividers(img, axis):
        """Return array indices of white horizontal or vertical lines."""
        blank_lines = np.where(np.all(img == 255, axis=axis))[0]
        filtered_idx = np.where(np.diff(blank_lines) != 1)[0]
        return blank_lines[filtered_idx]

    @staticmethod
    def sortContours(cnts, method="left-to-right"):
        """Return sorted countours."""
        reverse = False
        k = 0
        if method in ['right-to-left', 'bottom-to-top']:
            reverse = True
        if method in ['top-to-bottom', 'bottom-to-top']:
            k = 1
        b_boxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, b_boxes) = zip(*sorted(zip(cnts, b_boxes),
                                      key=lambda b: b[1][k],
                                      reverse=reverse))
        return (cnts, b_boxes)


if __name__ == "__main__":
    input_directory = r'Crop_Images'
    tcr = TabelCellRecognition(input_directory)
    tcr.processor()
