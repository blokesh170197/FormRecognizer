# table column detection

import os
import warnings
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as im
import torch
import torchvision

from pathlib import Path
from copro.core.logger import logger

warnings.filterwarnings('ignore')


class TableColumnDetection:
    # The init method or constructor
    def __init__(self, input_file, output_dir, table_column_model):
        # Instance Variable
        self.input_file = input_file
        self.output_dir = output_dir
        self.table_column_model = table_column_model

    """  table column detection """
    def table_column_detection(self):
        logger.info("TABLE COLUMN DETECTION START")
        table_column_detection_path = "table_column_detection"
        table_column_detection_path = os.path.join(self.output_dir, table_column_detection_path)
        os.makedirs(table_column_detection_path, exist_ok=True)

        # get a file name and file extension
        file_name = Path(self.input_file).stem
        file_extension = Path(self.input_file).suffix

        table_column_detection_path = os.path.join(table_column_detection_path, file_name)
        os.makedirs(table_column_detection_path, exist_ok=True)

        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        model = torch.load(self.table_column_model)
        input_image = im.imread(self.input_file)
        input_img = torchvision.transforms.functional.to_tensor(input_image).to(device)
        table_column_tensors = model([input_img])[0]["boxes"]
        prediction = table_column_tensors.data.cpu().numpy()

        count = 0
        input_file = im.imread(self.input_file)

        for table_tensor in prediction:
            table_tensor = [int(i) for i in table_tensor]
            cv2.imwrite(f'{table_column_detection_path}/{file_name}_{count}.jpg',
                        input_image[table_tensor[1]:table_tensor[3], table_tensor[0]:table_tensor[2]])
            images = cv2.rectangle(input_file, (table_tensor[0], table_tensor[1]), (table_tensor[2], table_tensor[3]),
                                  (255, 0, 0), 2)
            count += 1

            plt.figure(figsize=(15, 8))
            plt.imshow(images, cmap='gray')
            plt.title('Table Column Detection')
            plt.show()

        logger.info("TABLE COLUMN DETECTION END")

        return table_column_detection_path


