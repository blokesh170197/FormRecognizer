# table detection

import os
import warnings
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from PIL import Image
from copro.core.logger import logger

warnings.filterwarnings('ignore')


class TableDetection:
    # The init method or constructor
    def __init__(self, input_file, output_dir, table_model_dir, device, load_checkpoint, get_TableMasks, fixMasks, display, TableNet):
        # Instance Variable
        self.input_file = input_file
        self.output_dir = output_dir
        self.table_model_dir = table_model_dir
        self.device = device
        self.load_checkpoint = load_checkpoint
        self.get_TableMasks = get_TableMasks
        self.fixMasks = fixMasks
        self.display = display
        self.TableNet = TableNet

    """  table detection """

    def table_detection(self):
        logger.info("TABLE DETECTION START")

        table_detection_path = "table_detection"
        table_detection_path = os.path.join(self.output_dir, table_detection_path)
        os.makedirs(table_detection_path, exist_ok=True)

        # get a file name and file extension
        file_name = Path(self.input_file).stem
        file_extension = Path(self.input_file).suffix

        table_detection_path = os.path.join(table_detection_path, file_name)
        os.makedirs(table_detection_path, exist_ok=True)

        model = self.TableNet(encoder='densenet', use_pretrained_model=True, basemodel_requires_grad=True)
        model = model.to(self.device)

        # load checkpoint
        _, _, _ = self.load_checkpoint(torch.load(self.table_model_dir), model)

        orig_image = Image.open(self.input_file).resize((1024, 1024))
        test_img = np.array(orig_image.convert('LA').convert("RGB"))
        table_out, column_out = self.get_TableMasks(test_img, model)
        self.display(test_img, table_out, title='')
        outputs = self.fixMasks(test_img, table_out, column_out)
        if outputs is None:
            print("No Tables Found")
        test_image = test_img[..., 0].reshape(1024, 1024).astype(np.uint8)

        image, table_boundRect, col_boundRects = outputs

        color = (0, 0, 255)
        thickness = 4

        t_image = test_image.copy()

        count = 0
        for x, y, w, h in table_boundRect:
            t_image = cv2.rectangle(t_image, (x, y), (x + w, y + h), color, thickness)
            cv2.imwrite(f'{table_detection_path}/"{file_name}_{count}.jpg', t_image[y:y + h, x:x + w])
            count += 1

        plt.figure(figsize=(15, 8))
        plt.imshow(t_image, cmap='gray')
        plt.title('Table Detection')
        plt.show()

        logger.info("TABLE DETECTION END")

        return table_detection_path

