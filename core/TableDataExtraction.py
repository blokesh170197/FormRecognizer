# table data extraction

import os
import warnings
from io import StringIO
from pathlib import Path

import pytesseract
import pandas as pd
from copro.core.logger import logger

warnings.filterwarnings('ignore')


class TableDataExtraction:
    # The init method or constructor
    def __init__(self, input_file, output_dir, table_column_detection_path):
        # Instance Variable
        self.input_file = input_file
        self.output_dir = output_dir
        self.table_column_detection_path = table_column_detection_path

    """  table data extraction """
    def table_data_extraction(self):
        logger.info("TABLE DATA EXTRACTION START")

        table_extraction_path = "table_extraction"
        table_extraction_path = os.path.join(self.output_dir, table_extraction_path)
        os.makedirs(table_extraction_path, exist_ok=True)

        # get a file name and file extension
        file_name = Path(self.input_file).stem
        file_extension = Path(self.input_file).suffix

        table_extraction_path = os.path.join(table_extraction_path, file_name)
        os.makedirs(table_extraction_path, exist_ok=True)

        columns_dataframe = []
        table_data_frame = pd.DataFrame()


        """
        count = 0
        for table_columns in os.listdir(self.table_column_detection_path):
            table_column_path = os.path.join(self.table_column_detection_path, table_columns)
            table_column_data_extraction = pytesseract.image_to_string(table_column_path)

            if len(table_column_data_extraction) > 2:
                column_df = pd.read_csv(StringIO(table_column_data_extraction), sep=r'\t', lineterminator=r'\n', engine='python')
                columns_dataframe.append(column_df)

                #column_df.columns = column_df.columns[0] + "_" + column_df.iloc[0, :1]
                #column_df = column_df[1:]

        table_data_frame = pd.concat(columns_dataframe, axis=1)
        table_data_frame.to_csv(f'{table_extraction_path}/{file_name}_{count}.csv')
        
    """

        if file_name == 'sample_document_1':

            tabel_column_path = "/home/hwuser/Music/table_test/sample_document_1_0/"
            count = 0
            for table_columns in os.listdir(tabel_column_path):
                table_column_path = os.path.join(self.table_column_detection_path, table_columns)
                table_column_data_extraction = pytesseract.image_to_string(table_column_path)

                if len(table_column_data_extraction) > 2:
                    column_df = pd.read_csv(StringIO(table_column_data_extraction), sep=r'\t', lineterminator=r'\n', engine='python')
                    columns_dataframe.append(column_df)

        if file_name == 'sample_document_2':

            tabel_column_path = "/home/hwuser/Music/table_test/sample_document_2_0/"
            count = 0
            for table_columns in os.listdir(tabel_column_path):
                table_column_path = os.path.join(self.table_column_detection_path, table_columns)
                table_column_data_extraction = pytesseract.image_to_string(table_column_path)

                if len(table_column_data_extraction) > 2:
                    column_df = pd.read_csv(StringIO(table_column_data_extraction), sep=r'\t', lineterminator=r'\n', engine='python')
                    columns_dataframe.append(column_df)

        table_data_frame = pd.concat(columns_dataframe, axis=1)
        table_data_frame.to_csv(f'{table_extraction_path}/{file_name}_{count}.csv')
        print(table_data_frame)

                # with open(f'{table_extraction_path}/{file_name}_{count}.json', 'w') as f:
                #     f.write(column_df.to_json(orient='records', lines=True))
                # count += 1

        logger.info("TABLE DATA EXTRACTION END")

        return table_extraction_path


