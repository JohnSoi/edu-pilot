import secrets
import string

from passlib.context import CryptContext

from app.core.config import Settings, get_settings
from app.schemas.security import TokenResponse, TokenData
from .consts import BCRYPT_ROUNDS, TokenType, TOKEN_TEXT_TYPE, ADMIN_ROLE_CODE
from .utils import create_access_token, create_refresh_token, verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=BCRYPT_ROUNDS)
settings: Settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_random_password(length=settings.PASSWORD_MIN_LENGTH) -> str:
    alphabet: str = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_tokens(user_id: int, role_code: str, branch_id: int | None = None) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user_id, role_code, branch_id),
        refresh_token=create_refresh_token(user_id, role_code, branch_id),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


def verify_access_token(token: str) -> TokenData | None:
    return verify_token(token, TokenType.ACCESS)


def verify_refresh_token(token: str) -> TokenData | None:
    return verify_token(token, TokenType.REFRESH)


def refresh_access_token(refresh_token: str) -> TokenResponse | None:
    token_data: TokenData | None = verify_refresh_token(refresh_token)

    if not token_data:
        return None

    return create_tokens(token_data.user_id, token_data.role_code, token_data.branch_id)


def extract_token_from_header(authorization: str) -> str | None:
    if not authorization:
        return None

    parts: list[str] = authorization.split(" ")

    if len(parts) != 2 or parts[0].lower() != TOKEN_TEXT_TYPE:
        return None

    return parts[1]


def get_token_bearer_string(token: str) -> str:
    return f"{TOKEN_TEXT_TYPE.title()} {token}"


def has_role(token_data: TokenData, allowed_roles: list[str]) -> bool:
    return token_data.role_code in allowed_roles


def check_branch_access(token_data: TokenData, target_branch_id: int) -> bool:
    if token_data.role_code == ADMIN_ROLE_CODE:
        return True

    return target_branch_id == token_data.branch_id
