import secrets
from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import Settings, get_settings
from app.schemas.security import TokenData

from .consts import REFRESH_TOKEN_LENGTH, TokenType

settings: Settings = get_settings()


def create_access_token(
    user_id: int,
    role_code: str,
    branch_id: int | None = None,
    expires_delta: timedelta | None = None,
    extra_data: dict | None = None,
) -> str:
    return _create_token(user_id, role_code, branch_id, expires_delta, {**extra_data, "type": TokenType.ACCESS})


def create_refresh_token(
    user_id: int,
    role_code: str,
    branch_id: int | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    return _create_token(
        user_id,
        role_code,
        branch_id,
        expires_delta,
        {"type": TokenType.REFRESH, "jti": secrets.token_urlsafe(REFRESH_TOKEN_LENGTH)},
    )


def verify_token(token: str, token_type: TokenType) -> TokenData | None:
    token_data: TokenData | None = _decode_token(token)

    if not token_data:
        token_data: TokenData | None = _decode_token(token, False)

        if not token_data or token_data.type != token_type:
            return None

    return token_data


def _create_token(
    user_id: int,
    role_code: str,
    branch_id: int | None = None,
    expires_delta: timedelta | None = None,
    extra_data: dict | None = None,
) -> str:
    now: datetime = datetime.now(UTC)
    expire: datetime = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode: dict = {"sub": str(user_id), "role_code": role_code, "iat": now, "exp": expire}

    if branch_id:
        to_encode["branch_id"] = branch_id

    if extra_data:
        to_encode.update(extra_data)

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def _decode_token(token: str, verify_exp: bool = True) -> TokenData | None:
    try:
        payload: dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": verify_exp}
        )

        if not all(map(bool, (payload.get(field) for field in ("user_id", "role_code", "type")))):
            return None

        return TokenData(
            user_id=payload.get("user_id"),
            role_code=payload.get("role_code"),
            branch_id=payload.get("branch_id"),
            type=payload.get("type"),
        )
    except Exception:
        return None
