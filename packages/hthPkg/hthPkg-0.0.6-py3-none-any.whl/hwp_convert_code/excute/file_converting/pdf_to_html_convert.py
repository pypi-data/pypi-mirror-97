import threading
import time

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

class PDFConvert(threading.Thread):
    def __init__(self, target_file_name, save_location, replace_extension="html", password=""):
        pass