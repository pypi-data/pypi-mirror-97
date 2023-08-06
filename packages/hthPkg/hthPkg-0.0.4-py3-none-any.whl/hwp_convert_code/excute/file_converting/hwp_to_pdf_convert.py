import copy
import os
import subprocess
import threading

from hwp_convert_code.excute.error_manage.hwp_convert_error import RegistryRegistrationError

class HwpToPdfConvert(threading.Thread):

    def __init__(self, target_file_name, save_location, replace_extension="html", password=""):
        pass