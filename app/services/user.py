from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from app.models.model import User
from app.schemas.pagination import PageParams, PagedResponseSchema
from app.schemas.schema import UserSignUpRequest, UserSchema, UserUpdateRequest, UserSignInRequest
from app.utils.pagination import Pagination
from app.utils.utils import get_hash_password
import logging
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound


class UserService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def add_user(self, user: UserSignUpRequest) -> UserSchema:
            hashed_password = get_hash_password(user.password)
            data = user.dict(exclude={"password"})
            data["hashed_password"] = hashed_password
            new_user = User(**data)
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return UserSchema.from_orm(new_user)


    async def get_all_users(self, page_params: PageParams) -> PagedResponseSchema:
        pagination = Pagination(User, self.session,page_params)
        return await pagination.get_pagination()

    async def get_user_by_id(self, user_id: int)-> Optional[UserSchema] :
                try:
                    stmt = select(User).filter_by(id=user_id)
                    result = await self.session.execute(stmt)
                    user = result.scalar_one()
                    return UserSchema.from_orm(user)
                except SQLAlchemyError as e:
                    self.logger.error(f"get user by id: {str(e)}")
                    return None


    async def update_user(self,user_id: int, user: UserUpdateRequest):
        data = user.dict(exclude={'updated_at'})
        if data.get("hashed_password"):
            hashed_password = get_hash_password(data["hashed_password"])
            data["hashed_password"] = hashed_password
        current_user = await self.session.get(User, user_id)
        for key, value in data.items():
            setattr(current_user, key, value)
        current_user.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(current_user)
        return UserUpdateRequest.from_orm(current_user)


    async def delete_user(self, id: int):
            stmt = delete(User).filter_by(id=id)
            await self.session.execute(stmt)
            await self.session.commit()
            return True

    async def check_user_email(self,user:UserSignUpRequest):
        stmt = select(User).where(User.email == user.email)
        result = await self.session.execute(stmt)
        exist = result.scalars().all()
        if exist:
            return True
        return False


    async def get_user_by_email(self, email):
        stmt = select(User).where(User.email == email)
        try:
            result = await self.session.execute(stmt)
            current_user = result.scalar_one()
            return UserSignInRequest.from_orm(current_user)
        except NoResultFound:
            return None






