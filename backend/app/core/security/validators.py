import string

from app.core.config import Settings, get_settings

settings: Settings = get_settings()


def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return False, f"Длинна пароля должна быть не менее {settings.PASSWORD_MIN_LENGTH}"

    if not any(c.isupper() for c in password):
        return False, "Хотя бы один символ должен быть в верхнем регистре"

    if not any(c.islower() for c in password):
        return False, "Хотя бы один символ должен быть в нижнем регистре"

    if not any(c.isdigit() for c in password):
        return False, "Хотя бы один символ должен быть числом"

    if not any(c in string.punctuation for c in password):
        return False, "Должен быть хотя бы один спецсимвол"

    return True, ""
