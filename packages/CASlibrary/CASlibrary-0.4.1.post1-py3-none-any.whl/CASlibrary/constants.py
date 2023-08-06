from enum import Enum


class LogSeverity(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5


class AlarmType(Enum):
    ZVEI = "zvei"
    FAX = "fax"
    SDS = "sds"
