from pydantic import BaseModel, Field


class RoleCreateData(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    code: str = Field(..., min_length=3, max_length=10)
