from pydantic import BaseModel, field_validator
from typing import Optional
import datetime

class UserSchema(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    hashed_password: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False


class UserSignInRequest(BaseModel):
    email: str
    hashed_password: str


class UserSignUpRequest(BaseModel):
    email: str
    firstname: str
    lastname: str
    hashed_password: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False




class UserUpdateRequest(BaseModel):
    email: str
    firstname: str
    lastname: str
    hashed_password: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False
    updated_at: Optional[datetime.datetime] = None


class UserDetailResponse(BaseModel):
    description: Optional[str] = None
    is_superuser: Optional[bool] = False


class UsersListResponse(BaseModel):
    firstname: str
    lastname: str


