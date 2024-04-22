from app.models.model import User
from app.schemas.schema import UserSignUpRequest
from app.db.database import async_session_maker
from app.utils.utils import get_hash_password
from sqlalchemy import select

class UserService:
    async def add_user(self,user: UserSignUpRequest) -> User:
        hashed_password = get_hash_password(user.hashed_password).lower()
        data = user.model_dump(exclude_unset=True)
        data["hashed_password"] = hashed_password
        new_user = User(**data)
        print('***',new_user)
        async with async_session_maker() as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        return new_user


    async def get_all_users(self):
        stmt = select(User)
        async with async_session_maker() as session:
            users = await session.execute(stmt)
        return users
