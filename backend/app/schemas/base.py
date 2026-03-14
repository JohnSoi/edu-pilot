from pydantic import BaseModel


class AppStatusResponse(BaseModel):
    app_start: bool
    db_connecting: bool
    db_data: dict
    env: str

    has_user_admin: bool
    has_all_roles: bool
