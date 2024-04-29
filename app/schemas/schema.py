from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar
import datetime



DataT = TypeVar('DataT')

class UserSchema(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False

    class Config:
        from_attributes = True


class UserSignInRequest(BaseModel):
    email: str
    hashed_password: str

    class Config:
        from_attributes = True


class UserSignUpRequest(BaseModel):
    email: str
    firstname: str
    lastname: str
    password: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False

    class Config:
        from_attributes = True




class UserUpdateRequest(BaseModel):
    email: str
    firstname: str
    lastname: str
    hashed_password: str
    description: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    description: Optional[str] = None
    is_superuser: Optional[bool] = False


class UsersListResponse(BaseModel):
    firstname: str
    lastname: str


class MyResponse(BaseModel, Generic[DataT]):
    status_code: str
    result: Any



