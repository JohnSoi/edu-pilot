from .consts import VERSION_DELIMITER, VERSION_PART_LENGTH, VERSION_PARTS_COUNT
from .exceptions import EmptyVersion, InvalidVersion


def get_valid_app_version(version: str) -> str:
    if not version:
        raise EmptyVersion()

    if not isinstance(version, str) or VERSION_DELIMITER not in version:
        raise InvalidVersion(version)

    version_part: list[str] = version.split(VERSION_DELIMITER)

    if len(version_part) != VERSION_PARTS_COUNT or (
        any(not i.isdigit() or len(i) != VERSION_PART_LENGTH for i in version_part)
    ):
        raise InvalidVersion(version)

    return version
