
from sqlalchemy import Column, Integer, String, Boolean, MetaData
from sqlalchemy.orm import declarative_base, validates

from app.utils.exceptions import EmailUpdateNotAllowed, UpdateException

Base = declarative_base()
metadata = MetaData()


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password: str = Column(String)
    description: str = Column(String)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)

    @validates('email', 'lastname', 'description', 'is_active', 'is_superuser')
    def validate_changes(self, key, value):
        if self.id is not None:
            existing_value = getattr(self, key)
            if value != existing_value:
                raise UpdateException(f"{key}")
        return value


    def __str__(self):
        return f"User: id: {self.id}, name: {self.firstname} {self.lastname}"

    def __repr__(self):
        return f"User: id: {self.id}, name: {self.firstname} {self.lastname}"
