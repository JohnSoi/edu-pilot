from fastapi import status

from app.exceptions.base import BaseAppException


class NoAuthException(BaseAppException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAILS = "Пользователь не авторизован"


class InvalidToken(BaseAppException):
    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DETAILS = "Невалидный токен"


class AccessDenied(BaseAppException):
    _STATUS_CODE = status.HTTP_403_FORBIDDEN
    _DETAILS = "У вас недостаточно прав для выполнения данного действия"
