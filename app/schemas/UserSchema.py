from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field, constr


class UserLoginOrRegisterSchema(BaseModel):
    username: Annotated[str, constr(min_length=1, max_length=50)]
    email: Annotated[str, constr(min_length=1, max_length=50)]
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: Annotated[str, constr(min_length=1, max_length=50)]
    email: Annotated[str, constr(min_length=1, max_length=50)]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

class ResetPasswordFormat(BaseModel):
    username: Annotated[str, constr(min_length=1, max_length=50)]
    email: Annotated[str, constr(min_length=1, max_length=50)]
    oldPassword: str
    newPassword: str