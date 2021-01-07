from rest_framework.exceptions import APIException


class invalidCredentialsLogin(APIException):
    status_code = 401
    default_detail = "Unable to read file."
    default_code = "unreadable_csv_file"