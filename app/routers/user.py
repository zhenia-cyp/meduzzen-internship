from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.schemas.authentication import Token
from app.services.authentication import AuthService
from app.services.user import UserService
from app.schemas.pagination import PagedResponseSchema, PageParams
from app.schemas.schema import UserSignUpRequest, UserSchema, UserUpdateRequest, MyResponse, UserSignInRequest
from fastapi import HTTPException
from fastapi.security import HTTPBearer


router = APIRouter()
token_auth_scheme = HTTPBearer()


@router.post("/register/", response_model=UserSchema)
async def add_user(user: UserSignUpRequest, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    email = await user_service.check_user_email(user)
    if email:
         raise HTTPException(status_code=400, detail="User with this email already exists")
    user = await user_service.add_user(user)
    return user


@router.post("/login/", response_model=MyResponse[Token])
async def login(user: UserSignInRequest,session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    current_user = await user_service.get_user_by_email(user.email)
    if current_user is None:
        raise HTTPException(status_code=400, detail="Incorrect email")
    auth_service = AuthService(session)
    access_data = await auth_service.authenticate_user(user, current_user)
    if access_data is False:
         raise HTTPException(status_code=400,detail="Incorrect password")
    return MyResponse(status_code='200',message="ОК",result=access_data)


@router.get("/me", response_model=UserSignInRequest)
async def get_me(token: str = Depends(token_auth_scheme),session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token)
    return user



@router.get("/users/", response_model=PagedResponseSchema[UserSchema])
async def all_users(session: AsyncSession = Depends(get_async_session), page_params: PageParams = Depends(PageParams)):
    user_service = UserService(session)
    users = await user_service.get_all_users(page_params)
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