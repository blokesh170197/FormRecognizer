# auto rotation

import os
import warnings
import cv2
import pytesseract
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.ndimage import rotate as rotation
from copro.core.logger import logger

warnings.filterwarnings('ignore')


class AutoRotation:

    # The init method or constructor
    def __init__(self, input_file, output_dir, image_conversion_path):

        # Instance Variable
        self.input_file = input_file
        self.output_dir = output_dir
        self.image_conversion_path = image_conversion_path

    """   Auto Rotation  """

    def auto_rotation(self):

        logger.info("AUTO ROTATION START")

        # create a directory for Auto Rotation
        auto_rotation_path = "auto_rotation"
        auto_rotation_path = os.path.join(self.output_dir, auto_rotation_path)
        os.makedirs(auto_rotation_path, exist_ok=True)

        # get a file name and file extension
        file_name = Path(self.input_file).stem
        file_extension = Path(self.input_file).suffix

        auto_rotation_path = os.path.join(auto_rotation_path, file_name)
        os.makedirs(auto_rotation_path, exist_ok=True)

        def float_convertor(x):
            if x.isdigit():
                out = float(x)
            else:
                out = x
            return out

        def tesseract_find_rotation(img):
            img = cv2.imread(img) if isinstance(img, str) else img
            k = pytesseract.image_to_osd(img)
            output = {i.split(":")[0]: float_convertor(i.split(":")[-1].strip()) for i in k.rstrip().split("\n")}
            img_rotated = rotation(img, 360 - output["Rotate"])
            cv2.imwrite(auto_rotation_path + "/" + files, img_rotated)

            plt.figure(figsize=(15, 8))
            plt.imshow(img_rotated, cmap='gray')
            plt.title('Auto Rotation')
            plt.show()
            return output

        angles = []

        for files in os.listdir(self.image_conversion_path):
            rotated_images = os.path.join(self.image_conversion_path, files)
            angle = tesseract_find_rotation(rotated_images)
            angles.append({files: angle})

        logger.info("AUTO ROTATION END")

        return auto_rotation_path


