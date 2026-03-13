from typing import Any


class InvalidCorsValue(ValueError):
    def __init__(self, value: Any) -> None:
        super().__init__(f"Невалидное значение CORS: {value}")


class EmptyVersion(ValueError):
    def __init__(self) -> None:
        super().__init__("Версия не может быть пустой строкой")


class InvalidVersion(ValueError):
    def __init__(self, version: str) -> None:
        super().__init__(f"Невалидная версия: {version}. Версия должна быть в формате 00.00")


class EmptyDbSettings(ValueError):
    def __init__(self) -> None:
        super().__init__("Настройки базы данных не могут быть пустыми")
