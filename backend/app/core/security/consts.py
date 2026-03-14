from enum import StrEnum

BCRYPT_ROUNDS: int = 12


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


REFRESH_TOKEN_LENGTH: int = 16

TOKEN_TEXT_TYPE: str = "bearer"

ADMIN_ROLE_CODE: str = "admin"
DIRECTOR_ROLE_CODE: str = "director"
