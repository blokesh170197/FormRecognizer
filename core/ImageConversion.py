# image conversion

import os
import warnings
import matplotlib.pyplot as plt

from pathlib import Path
from pdf2image import convert_from_path
from copro.core.logger import logger

warnings.filterwarnings('ignore')


class ImageConversion:

    # The init method or constructor
    def __init__(self, input_file, output_dir, paper_itemization_path):

        # Instance Variable
        self.input_file = input_file
        self.output_dir = output_dir
        self.paper_itemization_path = paper_itemization_path

    """   Image Conversion  """

    def pdf_to_image_conversion(self):

        logger.info("IMAGE CONVERSION START")

        # create a directory for image_conversion
        converted_image_dir_name = "image_conversion"
        image_conversion_path = os.path.join(self.output_dir, converted_image_dir_name)
        os.makedirs(image_conversion_path, exist_ok=True)

        # get a file name and file extension
        file_name = Path(self.input_file).stem
        file_extension = Path(self.input_file).suffix

        image_conversion_path = os.path.join(image_conversion_path, file_name)
        os.makedirs(image_conversion_path, exist_ok=True)

        count = 0

        for files in os.listdir(self.paper_itemization_path):

            itemized_papers = os.path.join(self.paper_itemization_path, files)

            # get a file name and file extension
            file_name = Path(itemized_papers).stem

            # image conversion
            images = convert_from_path(itemized_papers)
            for img_count in range(len(images)):
                images[img_count].save(f'{image_conversion_path}/{file_name}.jpg', 'JPEG')
                count = count + 1

                plt.figure(figsize=(15, 8))
                plt.imshow(images[img_count], cmap='gray')
                plt.title('Image Conversion')
                plt.show()

        logger.info("IMAGE CONVERSION END")

        return image_conversion_path


