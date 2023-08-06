class RegistryRegistrationError(Exception):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return f"'{self.arg}' Registry가 등록 되어있지 않습니다."

class ConvertSettingFileError(Exception):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return f"'{self.arg1}' paramter의 값이 '{self.arg2}'로 잘못되었습니다. "