from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

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

    def __str__(self):
       return f"{self.email} {self.firstname} {self.lastname} {self.hashed_password}"
