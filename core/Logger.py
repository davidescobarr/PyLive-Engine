from enum import Enum
from typing import Optional


class TypesLog(Enum):
    INFO = ''
    WARNING = ''
    ERROR = ''

TypesLog = Enum('TypesLog', ['INFO', 'WARNING', 'ERROR'])

class Logger:
    def __init__(self, path_file_log: Optional[str] = ""):
        self.path_file_log = path_file_log

    def log(self, text, type: Optional[TypesLog] = TypesLog.INFO) -> None:
        print(type.value.format(text))