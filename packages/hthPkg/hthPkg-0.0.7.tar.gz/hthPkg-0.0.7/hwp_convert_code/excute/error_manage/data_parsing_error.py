class NotAllowedExtensionError(Exception):
    def __init__(self, arg=None):
        self.arg = arg

    def __str__(self):
        return f"설정파일의 '변환전확장자' 옵션이 허용되지 않습니다."


class WrongFileExtensionError(Exception):
    def __init__(self, arg=None):
        self.arg = arg

    def __str__(self):
        return f"설정파일의 '원본파일형태' 옵션이 올바르지 않습니다. '원본파일형태' 옵션은 hwp 및 pdf 두가지의 옵션만 지원합니다."

class FileShapeNotFoundError(Exception):
    def __init__(self, arg=None):
        self.arg = arg

    def __str__(self):
        return f"설정파일의 '파일형태' 옵션이 존재하지 않습니다."

class WrongFileStructureError(Exception):
    def __init__(self, arg=None):
        self.arg = arg

    def __str__(self):
        return f"설정파일의 '파일형태' 옵션이 올바르지 않습니다."

class WrongSettingFileError(Exception):
    def __init__(self, arg=None):
        self.arg = arg

    def __str__(self):
        return f"설정파일의 'tag'값 또는 'name'값이 존재하지 않습니다."