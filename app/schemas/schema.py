from pydantic import BaseModel, field_validator
from typing import Optional
import datetime

class UserSchema(BaseModel):
    id: int
    user_email: str
    hashed_password: str
    user_firstname: str
    user_lastname: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False


class UserSignInRequest(BaseModel):
    user_email: str
    hashed_password: str


class UserSignUpRequest(BaseModel):
    user_email: str
    user_firstname: str
    user_lastname: str
    hashed_password: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False


class UserUpdateRequest(BaseModel):
    user_email: str
    user_firstname: str
    user_lastname: str
    hashed_password: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False
    updated_at: Optional[datetime.datetime] = None


class UserDetailResponse(BaseModel):
    description: Optional[str] = None
    is_superuser: Optional[bool] = False


class UsersListResponse(BaseModel):
    user_firstname: str
    user_lastname: str


