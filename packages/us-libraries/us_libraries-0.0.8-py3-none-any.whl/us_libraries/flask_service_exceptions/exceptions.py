from typing import Dict, Optional


class ServiceException(Exception):

    def __init__(self, message: Optional[str] = None, status_code: int = 500):
        self.status_code = status_code
        self.message = message if message else "BFF Error"

    def get_status_code(self) -> int:
        return self.status_code

    def to_dict(self) -> Dict:
        dto = {
            "status_code": self.status_code,
            "message": self.message
        }
        return dto


class ValidationException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        self.status_code = 400
        self.message = message if message else "Invalid value"


class RecordNotFoundException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        self.status_code = 404
        self.message = message if message else "Record not found"


class MethodNotAllowedException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        self.status_code = 405
        self.message = message if message else "Method Not Allowed"


class BadGatewayException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        self.status_code = 502
        self.message = message if message else "Bad Gateway"


class GatewayTimeoutException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        self.status_code = 504
        self.message = message if message else "Gateway Timeout"


class ServiceUnavailableException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        self.status_code = 503
        self.message = message if message else "Service Unavailable"


class ServiceErrorException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        self.status_code = 500
        self.message = message or "An Error occurred in the Service"
