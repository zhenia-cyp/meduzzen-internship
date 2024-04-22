from typing import List
from app.schemas.schema import UsersListResponse, UserSignUpRequest
from fastapi import APIRouter, Depends
from app.services.user import UserService
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/register/")
async def add_user(user: UserSignUpRequest, user_service = Depends(UserService)):
    await user_service.add_user(user)
    return JSONResponse({"status": "OK", "message": "A new user has registered"})


@router.get("/users/", response_model=List[UsersListResponse])
async def all_users(user_service = Depends(UserService)):
    users = await user_service.get_all_users()
    return users

