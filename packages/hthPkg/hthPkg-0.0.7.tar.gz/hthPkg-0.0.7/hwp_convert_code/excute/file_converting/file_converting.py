import os
import multiprocessing
import pickle

from multiprocessing import Process
from utility.file_finder import file_search

from hwp_convert_code.excute.error_manage.hwp_convert_error import ConvertSettingFileError
from hwp_convert_code.excute.file_converting.hwp_to_html_convert import HWPConvert
from hwp_convert_code.excute.file_converting.hwp_to_pdf_convert import HwpToPdfConvert
from hwp_convert_code.excute.file_converting.pdf_to_html_convert import PDFConvert
from hwp_convert_code.excute.error_manage.data_parsing_error import NotAllowedExtensionError
from utility.my_log import myLog

class DataConverting(multiprocessing.Process):
    def __init__(self, session_key, convert_before_file_location, convert_after_file_location):
        super(DataConverting, self).__init__()

        self.DATA_PARSING_SETTING_FILE_NAME = None
        self.DATA_PARSING_SETTING_FILE_LOCATION = None
        self._DATA_PARSING_SETTING_FILE_CONTENT = None

        self.CONVERT_BEFORE_FILE_LOCATION = convert_before_file_location
        self.CONVERT_BEFORE_EXTENSION = None
        self.CONVERT_AFTER_FILE_LOCATION = convert_after_file_location
        self.CONVERT_AFTER_EXTENSION = None

        self.NUMBER_OF_CONVERT_FILE = 0
        self.NUMBER_OF_THREADING = 1

        self.CONVERT_BEFORE_EXTENSION = "hwp"
        self.CONVERT_AFTER_EXTENSION = "html"

        self.log = myLog(project_name="hwp-parsing-api", run_file_location=__file__, save_file_location="hwp_convert_code/logs/file_convert_log")

        self.MULTI_METHOD = "multiprocess"
        self.NUMBER_OF_THREADING = 24
        self.NUMBER_OF_CONVERT_FILE = 0
        self.session_key = session_key
        self.work_process = {}

    def _execute_convert_file__multiprocess(self, file_type, convert_file_location, convert_after_file_location, replace_extension):
        data_convert_instance = HWPConvert(convert_file_location, convert_after_file_location, replace_extension=replace_extension)
        data_convert_instance.run()

    def _parsing_thread_scheduling(self, convert_file_location_list):
        end_work_count = 0
        now_executing_thread = 0
        data_convert_thread_list = []

        self.log.info(f"병렬처리 방법 : {self.MULTI_METHOD}\n")
        self.log.info(f"{self.MULTI_METHOD} 동작 수 : {self.NUMBER_OF_THREADING}\n")

        for convert_file_location in convert_file_location_list:
            file_extension = convert_file_location.split(".")[-1]
            if len(file_extension) > 4:
                file_extension = ""

            if (self.CONVERT_BEFORE_EXTENSION.lower() == "hwp" or self.CONVERT_BEFORE_EXTENSION.lower() == "all") and file_extension == "hwp":
                converted_file_list = file_search(self.CONVERT_AFTER_FILE_LOCATION, print_location=False)
                if convert_file_location.split("/")[-1] + ".html" in converted_file_list:
                    continue

                self.log.info(f"파일 변환 {self.MULTI_METHOD} 준비중.. [{convert_file_location}]")
                data_convert_instance = Process(target=self._execute_convert_file__multiprocess, args=('hwp', convert_file_location, self.CONVERT_AFTER_FILE_LOCATION, self.CONVERT_AFTER_EXTENSION))
                data_convert_thread_list.append(data_convert_instance)

            else:
                raise NotAllowedExtensionError

            self.log.info(f"파일 변환 {self.MULTI_METHOD} 시작 [{data_convert_thread_list[-1].name}]")

            data_convert_thread_list[-1].start()
            now_executing_thread += 1

            while True:
                convert_thread_alive_list = [[i_index, i.is_alive()] for i_index, i in enumerate(data_convert_thread_list)]
                convert_thread_alive_list.reverse()

                for thread_alive_info in convert_thread_alive_list:
                    if thread_alive_info[1] is False:
                        now_executing_thread -= 1
                        end_work_count += 1

                        self.work_process[self.session_key] = {
                            "all_process_number" : len(convert_file_location_list),
                            "complate_process_number" : end_work_count
                        }

                        with open("hwp_convert_code/pipeline.pl", "wb") as write_file:
                            pickle.dump(self.work_process, write_file)

                        self.log.info(f"파일 변환 {self.MULTI_METHOD} 종료 [{data_convert_thread_list[thread_alive_info[0]].name}]")

                        del data_convert_thread_list[thread_alive_info[0]]

                if now_executing_thread != self.NUMBER_OF_THREADING:
                    break

        for convert_thread in data_convert_thread_list:
            convert_thread.join()
            end_work_count += 1

            self.work_process[self.session_key] = {
                "all_process_number": len(convert_file_location_list),
                "complate_process_number": end_work_count
            }

            with open("hwp_convert_code/pipeline.pl", "wb") as write_file:
                pickle.dump(self.work_process, write_file)


    def run(self):
        self.log.info("----------데이터 변환 시작----------")
        if self.CONVERT_AFTER_EXTENSION == "html":
            self.log.info(" --> HWP/PDF to HTML")
            self._document_to_html()

        else:
            self.log.info("설정파일 에러")
            raise ConvertSettingFileError("변환후확장자", self.CONVERT_AFTER_EXTENSION)


    def _document_to_html(self):
        extension_list = []

        if self.CONVERT_BEFORE_EXTENSION == "all":
            extension_list = ["hwp", "pdf"]
        else:
            extension_list.append(self.CONVERT_BEFORE_EXTENSION)

        convert_file_location_list = file_search(self.CONVERT_BEFORE_FILE_LOCATION, extension=extension_list, include_in_directory=True)

        if len(convert_file_location_list) > self.NUMBER_OF_CONVERT_FILE and self.NUMBER_OF_CONVERT_FILE not in [None, "None", "null", "", 0]:
            convert_file_location_list = convert_file_location_list[:self.NUMBER_OF_CONVERT_FILE]

        self.work_process[self.session_key] = {
            "all_process_number": len(convert_file_location_list),
            "complate_process_number": 0
        }

        with open("hwp_convert_code/pipeline.pl", "wb") as write_file:
            pickle.dump(self.work_process, write_file)

        self._parsing_thread_scheduling(convert_file_location_list)

