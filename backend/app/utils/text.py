def camel_to_snake(values: str) -> str:
    snake_case: list[str] = []

    for i, char in enumerate(values):
        if char.isupper() and i > 0:
            snake_case.append("_")
        snake_case.append(char.lower())

    result: str = "".join(snake_case)

    if not result.endswith("s"):
        result += "s"

    return result
