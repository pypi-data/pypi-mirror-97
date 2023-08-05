from rest_framework.exceptions import APIException


class AuthenticationError(APIException):
    pass
