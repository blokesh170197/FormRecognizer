import os
import torch

# parent directory
PARENT_DIR = "/home/hwuser/Workspace/"

# table detection

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TABLE_MODEL_DIR = PARENT_DIR + "intics-asis/property-analytics/RnD/models/table_models/table_detection_densenet_model.pth.tar"
TABLE_COLUMNS_MODEL = PARENT_DIR + "intics-asis/property-analytics/RnD/models/table_models/table_column_detection_2.pth"

SEED = 0
LEARNING_RATE = 0.0001
EPOCHS = 100
BATCH_SIZE = 2
WEIGHT_DECAY = 3e-4
DATAPATH = PARENT_DIR + 'intics-asis/property-analytics/RnD/models/table_models/processed_data_v2.csv'