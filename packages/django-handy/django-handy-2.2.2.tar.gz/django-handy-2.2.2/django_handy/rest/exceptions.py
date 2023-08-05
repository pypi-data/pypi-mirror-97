from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ProcessingError(Exception):
    default_detail = 'An error occurred'

    def __init__(self, detail=None):
        if isinstance(detail, ProcessingError):
            detail = detail.detail
        self.detail = detail or self.default_detail

    def __repr__(self):
        return self.detail


class CommonException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Something was wrong with provided data'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail


def custom_exception_handler(exc, context):
    if isinstance(exc, ProcessingError):
        exc = CommonException(detail=exc.detail)
    return exception_handler(exc, context)
