from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.services.user import UserService
from app.schemas.schema import UserSignUpRequest, UserSchema,UserUpdateRequest,MyResponse

router = APIRouter()


@router.post("/register/", response_model=UserSchema)
async def add_user(user: UserSignUpRequest, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    user = await user_service.add_user(user)
    return user


@router.get("/users/", response_model=List[UserSchema])
async def all_users(session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    users = await user_service.get_all_users()
    return users


@router.get("/user/{user_id}/",response_model=MyResponse[UserSchema])
async def get_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    user = await user_service.get_user_by_id(user_id)
    return MyResponse(status_code='200',message="ОК",result=user)


@router.put("/user/edit/{user_id}/", response_model=MyResponse[UserSchema])
async def update_user(user_id: int, user: UserUpdateRequest, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    user = await user_service.update_user(user_id,user)
    return MyResponse(status_code="200",message="updated user",result=user)


@router.delete("/user/delete/{user_id}/", response_model=MyResponse[int])
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
     user_service = UserService(session)
     user = await user_service.delete_user(user_id)
     return MyResponse(status_code="200",message="Delete user",result=user)