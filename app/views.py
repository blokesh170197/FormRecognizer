import sys
import uuid
import logging
from pathlib import Path

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from rest_framework import status 

from copro.utils.config import INPUT_FILE, OUTPUT_DIR, PARENT_DIR
from core.ImageConversion import ImageConversion
from core.PaperItemization import PaperItemization
from core.AutoRotation import AutoRotation
from copro.core.FileDetails import getChecksum, getFileSize

logging.basicConfig(filename="running_info.log", format='%(asctime)s %(message)s', filemode='w')
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


class InformationExtraction(ViewSet):

    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

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

        except Exception as e:

            response["status"] = status.HTTP_404_NOT_FOUND
            response["informationExtraction"] = False
            logger.error(str(e))

        return Response(response)
