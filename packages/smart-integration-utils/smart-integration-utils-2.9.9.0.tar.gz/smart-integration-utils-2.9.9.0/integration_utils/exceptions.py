from rest_framework.exceptions import APIException


class InvalidDateParams(APIException):
    status_code = 422
    default_code = 'invalid_date'
    default_detail = 'Invalid date params.'


class ReportUpdating(APIException):
    status_code = 204


class DontHaveReportData(APIException):
    status_code = 406
    default_detail = 'Dont have reports for this integration'


class InvalidFieldsParam(APIException):
    status_code = 422
    default_code = 'invalid_fields'
    default_detail = 'Invalid fields param, fields must be a list'
