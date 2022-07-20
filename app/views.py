
""" import packages """

import os
import uuid
from pathlib import Path

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import DoAssetAttributionSerializer
from rest_framework import status

from copro.utils.config import PARENT_DIR
from copro.core.ImageConversion import ImageConversion
from copro.core.PaperItemization import PaperItemization
from copro.core.AutoRotation import AutoRotation
from copro.core.TableDetection import TableDetection
from copro.core.TableColumnDetection import TableColumnDetection
from copro.core.TableDataExtraction import TableDataExtraction
from copro.core.FileDetails import getChecksum, getFileSize

from copro.table.table_config import TABLE_MODEL_DIR, DEVICE, TABLE_COLUMNS_MODEL
from copro.table.utils import load_checkpoint, get_TableMasks, fixMasks, display
from copro.table.model import TableNet
from copro.core.logger import logger


class InformationExtraction(ViewSet):

    serializer_class = DoAssetAttributionSerializer

    def list(self, request):
        return Response("POST API")

    def create(self, request):
        response = {}
        try:

            input_file = PARENT_DIR + request.data.get('inputFilePath')
            output_dir = PARENT_DIR + request.data.get('outputDir')

            # get a file name and file extension
            file_name = Path(input_file).stem
            file_extension = Path(input_file).suffix

            file_size = getFileSize(input_file)
            file_checksum = getChecksum(input_file)

            paper_itemization = PaperItemization(input_file, output_dir)
            paper_itemization_path = paper_itemization.paper_itemization()

            image_conversion = ImageConversion(input_file, output_dir, paper_itemization_path)
            image_conversion_path = image_conversion.pdf_to_image_conversion()

            auto_rotation = AutoRotation(input_file, output_dir, image_conversion_path)
            auto_rotation_path = auto_rotation.auto_rotation()

            for auto_rotated_files in os.listdir(auto_rotation_path):
                auto_rotated_files = os.path.join(auto_rotation_path, auto_rotated_files)

                table_detection = TableDetection(auto_rotated_files, output_dir, TABLE_MODEL_DIR, DEVICE,
                                                 load_checkpoint, get_TableMasks, fixMasks, display, TableNet)
                table_detection_path = table_detection.table_detection()

                table_column_detection = TableColumnDetection(auto_rotated_files, output_dir, TABLE_COLUMNS_MODEL)
                table_column_detection_path = table_column_detection.table_column_detection()

                table_extraction = TableDataExtraction(input_file, output_dir, table_column_detection_path)
                table_extraction_path = table_extraction.table_data_extraction()

            response['status'] = status.HTTP_200_OK
            response['id'] = uuid.uuid1()

            response['inputFile'] = input_file
            response['inputFileName'] = file_name
            response['inputFileExtension'] = file_extension
            response['inputFileSizeInKb'] = file_size
            response['inputFileChecksum'] = file_checksum

            response["itemizedPaperPath"] = paper_itemization_path
            response["convertedImagePath"] = image_conversion_path
            response["autoRotationPath"] = auto_rotation_path

            response["detectedTablesPath"] = table_detection_path
            response["detectedTableColumnsPath"] = table_column_detection_path
            response["extractedTableContentsPath"] = table_extraction_path

        except Exception as e:

            response["status"] = status.HTTP_404_NOT_FOUND
            response["informationExtraction"] = False
            logger.error(str(e))

        return Response(response)
