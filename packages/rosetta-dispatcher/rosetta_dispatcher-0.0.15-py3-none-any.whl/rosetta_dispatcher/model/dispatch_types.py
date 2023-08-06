from enum import Enum


class DispatchRequestType(str, Enum):
    JSON = 'JSON'


class DispatchResponseStatus(str, Enum):
    OK = 'OK'
    TIMEOUT = 'TIMEOUT'
