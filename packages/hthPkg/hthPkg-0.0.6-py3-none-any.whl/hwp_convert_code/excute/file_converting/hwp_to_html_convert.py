import copy
import os
import glob
import subprocess
import threading
import zlib
from contextlib import closing
from functools import partial

from docopt import docopt
import config as cf

from hwp5.hwp5html import HTMLTransform, wrap_for_css, wrap_for_xml, open_dir
from hwp5.proc import rest_to_docopt, version, init_logger
from hwp5.utils import make_open_dest_file
from hwp5.xmlmodel import Hwp5File

from hwp_convert_code.excute.error_manage.hwp_convert_error import RegistryRegistrationError

'''
* HWP 문서를 Html 문서로 변환하는 프로그램
'''


class HWPConvert(threading.Thread):
    def __init__(self, target_file_name, save_location, replace_extension="html", password=""):
        self.CODEC = "utf-8"
        self.PASSWORD = password
        self.TARGET_FILE_NAME = target_file_name
        self.REPLACE_FILE_NAME = target_file_name.split("\\")[-1].split(".hwp")[0] + "." + replace_extension
        self.SAVE_LOCATION = save_location # if save_location[-1] in ["\\", "/"] else save_location + "/"
        self.EXTENSION = replace_extension
        self.HWP_SECURE_REGISTRY_NAME = "FilePathCheckerModule"

        threading.Thread.__init__(self)

    # 현재 실행중인 프로세스의 정보를 가져옴
    def __get_execute_process_list(self):
        process_dict = {}
        all_process_list = [line.split() for line in
                            subprocess.check_output(["tasklist", "/V"], encoding="cp949").splitlines()]

        for i in all_process_list[3:]:
            process_dict.setdefault(i[0], [])
            in_list = process_dict.get(i[0])

            name_index = 0
            origin_info = copy.deepcopy(i)
            for j_index, j in enumerate(reversed(origin_info)):
                if j.find(":") != -1:
                    name_index = len(origin_info) - j_index
                    break

            process_name = " ".join(i[name_index:])

            for j in origin_info[name_index:]:
                del i[name_index]
            i.append(process_name)

            in_list.append(i)

        return process_dict

    def __get_process_name(self):
        filename = self.TARGET_FILE_NAME.split("/")[-1]
        file_location = self.TARGET_FILE_NAME.replace(filename, "").replace("/", "\\")
        return f"{filename} [{file_location}] - 한글"

    def hwp_to_html(self):
        __doc__ = '''HWPv5 to HTML converter

        Usage::

            hwp5html [options] <hwp5file>
            hwp5html [options] <hwp5file> --html
            hwp5html [options] <hwp5file> --css
            hwp5html -h | --help
            hwp5html --version

        Options::

            -h --help           Show this screen
            --version           Show version
            --loglevel=<level>  Set log level.
            --logfile=<file>    Set log file.

            --output=<output>   Output file / directory'''

        doc = rest_to_docopt(__doc__)
        args = docopt(doc, argv=[self.TARGET_FILE_NAME], version=version)
        init_logger(args)

        hwp5path = args['<hwp5file>']

        html_transform = HTMLTransform()

        open_dest = make_open_dest_file(args['--output'])
        if args['--css']:
            transform = html_transform.transform_hwp5_to_css
            open_dest = wrap_for_css(open_dest)

        elif args['--html']:
            transform = html_transform.transform_hwp5_to_xhtml
            open_dest = wrap_for_xml(open_dest)

        else:
            transform = html_transform.transform_hwp5_to_dir
            dest_path = self.SAVE_LOCATION + self.REPLACE_FILE_NAME

            if not (os.path.isdir(dest_path)):
                os.makedirs(os.path.join(dest_path))

            if not dest_path:
                dest_path = os.path.splitext(os.path.basename(hwp5path))[0]
            open_dest = partial(open_dir, dest_path)

        with closing(Hwp5File(hwp5path)) as hwp5file:
            with open_dest() as dest:
                transform(hwp5file, dest)

    def run(self):
        self.hwp_to_html()


def run_list(path):

    if path == 'test':
        config_path = cf.test_path
    elif path == 'linux':
        config_path = cf.path
    else :
        print('path error')

    input_path = config_path.targetPattern
    output_path = config_path.output_path

    res = glob.glob(input_path)

    for result in res:
        print(result)
        try:
            hwp_convert = HWPConvert(target_file_name=result,
                                     save_location=output_path,
                                     replace_extension="html")
            hwp_convert.run()
        except zlib.error as e:
            print(e)

    # for root, dirs, files in os.walk(output_path):
    #     rootpath = os.path.join(os.path.abspath(output_path), root)
    #
    #     for file in files:
    #         filepath = os.path.join(rootpath, file)
    #         res.append(filepath)
    #
    #     for result in res:
    #         print(result)
    #         file_name = result.split("/")[-1]
    #         file_path = os.path.join()