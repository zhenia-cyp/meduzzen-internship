
from sqlalchemy import Column, Integer, String, Boolean,  ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, validates
from app.utils.exceptions import UpdateException

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


class Invitation(Base):
    __tablename__ = "Invitation"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("User.id"))
    recipient_id = Column(Integer, ForeignKey("User.id"))
    company_id = Column(Integer, ForeignKey("Company.id"))
    is_accepted: bool = Column(Boolean, default=None)

    def __str__(self):
        return (f"Invitation: id: {self.id}, sender_id: {self.sender_id}, "
                f"recipient_id: {self.recipient_id}, is_accepted: {self.is_accepted}")

    def __repr__(self):
        return (f"Invitation: id: {self.id}, "
                f"sender_id: {self.sender_id}, recipient_id: {self.recipient_id}, is_accepted: {self.is_accepted}")


class Request(Base):
    __tablename__ = "Request"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("User.id"))
    company_id = Column(Integer, ForeignKey("Company.id"))
    is_accepted: bool = Column(Boolean, default=None)

    def __str__(self):
        return (f"Request: id: {self.id}, sender_id: {self.sender_id}, company_id: {self.company_id}, "
                f"is_accepted: {self.is_accepted}")

    def __repr__(self):
        return (f"Request: id: {self.id}, sender_id: {self.sender_id}, "
                f"company_id: {self.company_id}, is_accepted: {self.is_accepted}")


class Member(Base):
    __tablename__ = "Member"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    role = Column(String)
    company_id = Column(Integer, ForeignKey("Company.id"))

    def __str__(self):
        return f"Member: id: {self.id}, user_id: {self.user_id}, role: {self.role}, company_id: {self.company_id}"

    def __repr__(self):
        return f"Member: id: {self.id}, user_id: {self.user_id}, role: {self.role}, company_id: {self.company_id}"
