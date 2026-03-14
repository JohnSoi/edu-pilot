from enum import StrEnum

BCRYPT_ROUNDS: int = 12


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


REFRESH_TOKEN_LENGTH: int = 16

TOKEN_TEXT_TYPE: str = "bearer"

ADMIN_ROLE_CODE: str = "admin"
DIRECTOR_ROLE_CODE: str = "director"
MANAGER_ROLE_CODE: str = "manager"
MANAGER_LEARNING_ROLE_CODE: str = "l_manager"
TEACHER_ROLE_CODE: str = "teacher"
STUDENT_ROLE_CODE: str = "student"
