# paper itemization

import os
import warnings

from pathlib import Path
from PyPDF2 import PdfFileWriter, PdfFileReader
from copro.core.logger import logger

warnings.filterwarnings('ignore')


class PaperItemization:
    # The init method or constructor
    def __init__(self, input_file, output_dir):
        # Instance Variable
        self.input_file = input_file
        self.output_dir = output_dir

    """  paper itemization"""
    def paper_itemization(self):
        logger.info("PAPER ITEMIZATION START")

        # create a directory for paper itemization
        itemized_dir_name = "paper_itemization"
        paper_itemization_path = os.path.join(self.output_dir, itemized_dir_name)
        os.makedirs(paper_itemization_path, exist_ok=True)

        # get a file name and file extension
        file_name = Path(self.input_file).stem

        paper_itemization_path = os.path.join(paper_itemization_path, file_name)
        os.makedirs(paper_itemization_path, exist_ok=True)

        # pdf file reader
        input_pdf = PdfFileReader(open(self.input_file, "rb"))

        for page_no in range(input_pdf.numPages):
            # pdf file writer
            output = PdfFileWriter()
            output.addPage(input_pdf.getPage(page_no))
            with open(f'{paper_itemization_path}/{file_name}_%s.pdf' % page_no, "wb") as output_stream:
                output.write(output_stream)

        # paper itemization outputs
        paper_itemization_output = dict()
        paper_itemization_output['paperItemizationPath'] = paper_itemization_path

        logger.info("PAPER ITEMIZATION END")

        return paper_itemization_path


