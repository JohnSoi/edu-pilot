from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _DETAILS: str = "Внутренняя ошибка сервера"

    def __init__(self, details: str | None = None) -> None:
        super().__init__(detail=details or self._DETAILS, status_code=self._STATUS_CODE)


class ValidationError(BaseAppException):
    _STATUS_CODE = status.HTTP_400_BAD_REQUEST
