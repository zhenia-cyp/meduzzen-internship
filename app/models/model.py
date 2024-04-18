from sqlalchemy import Column, Integer, String, Boolean
from app.schemas.schema import UserSchema
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

Base = declarative_base()
metadata = MetaData()

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    user_email = Column(String)
    user_firstname = Column(String)
    user_lastname = Column(String)
    hashed_password: str = Column(String)
    description: str = Column(String)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)

