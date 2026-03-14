from datetime import datetime

from pydantic import BaseModel

from app.core.security.consts import TOKEN_TEXT_TYPE, TokenType


class TokenPayload(BaseModel):
    sub: str
    role_code: str
    branch_id: int | None = None
    type: str
    exp: datetime
    iat: datetime
    jti: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = TOKEN_TEXT_TYPE
    expires_in: int


class TokenData(BaseModel):
    user_id: int
    role_code: str
    branch_id: int | None = None
    type: TokenType
    email: str | None = None
    permissions: list[str] | None = None
