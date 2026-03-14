from typing import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import has_role, verify_access_token
from app.exceptions.auth import AccessDenied, InvalidToken, NoAuthException
from app.schemas.security import TokenData

security: HTTPBearer = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> TokenData:
    if not credentials:
        raise NoAuthException()

    token: str = credentials.credentials
    token_data: TokenData | None = verify_access_token(token)

    if not token_data:
        raise InvalidToken()

    return token_data


def require_roles(allowed_roles: list[str]) -> Callable:
    def role_dependency(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if not has_role(current_user, allowed_roles):
            raise AccessDenied()

        return current_user

    return role_dependency
