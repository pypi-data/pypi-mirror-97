## 대상정의 세팅파일 관련 에러
class PreprocessShapeError(Exception):
    def __str__(self):
        return '클랜징 설정파일(preprocessing_shape.json)의 "전처리형태" 값이 존재하지 않습니다.'


class CleansingFormFileContentError(Exception):
    def __str__(self):
        return '클랜징 설정파일(preprocessing_shape.json)의 "전처리대상정의" 또는 "전처리대상매핑" 값이 존재하지 않습니다.'


class ColumnNameNotMatchedError(Exception):
    def __str__(self):
        return '설정파일의 Database Column 명이 올바르지 않습니다.'


class TableNameNotFoundError(Exception):
    def __str__(self):
        return '클랜징 설정파일(preprocessing_shape.json)의 "테이블 명" 값이 존재하지 않습니다.'


## 전처리형태 세팅파일 관련 에러
class PreprocessTargetDefError(Exception):
    def __str__(self):
        return '클랜징 설정파일(preprocessing_target_def.json)의 "대상정의" 값이 존재하지 않습니다.'


## ETC
class SQLProgrammingError(Exception):
    def __str__(self):
        return 'SQL이 올바르지 않습니다.'


class PreprocessShapeNotMatchedError(Exception):
    def __str__(self):
        return '설정파일의 전처리 형태가 매칭되지 않습니다.'