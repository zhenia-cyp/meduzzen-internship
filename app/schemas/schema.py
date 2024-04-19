from pydantic import BaseModel, field_validator
from typing import Optional
import datetime

class UserSchema(BaseModel):
    id: int
    email: str
    hashed_password: str
    firstname: str
    lastname: str
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

    @field_validator('hashed_password')
    def password_validation(cls, hashed_password):
        if len(hashed_password) < 7:
            raise ValueError('Password must be at least 7 characters long')

        if not hashed_password:
            raise ValueError('Password cannot be blank')



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


