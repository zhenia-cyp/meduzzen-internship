
from sqlalchemy import Column, Integer, String, Boolean,  ForeignKey, MetaData
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


class Company(Base):
    __tablename__ = "Company"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("User.id"))
    name = Column(String)
    description = Column(String)
    city = Column(String)
    phone = Column(String)
    link = Column(String)
    company_avatar = Column(String)
    is_visible: bool = Column(Boolean, default=False)

    @validates('city', 'phone', 'link', 'company_avatar')
    def validate_changes(self, key, value):
        if self.id is not None:
            existing_value = getattr(self, key)
            if value != existing_value:
                raise UpdateException(f"{key}")
        return value

    def __str__(self):
        return f"Company: id: {self.id}, name: {self.name}, city: {self.city}"

    def __repr__(self):
        return f"Company: id: {self.id}, name: {self.name}, city: {self.city}"
