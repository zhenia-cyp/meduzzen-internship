from pydantic import BaseModel
from typing import Optional
import datetime

class CompanySchema(BaseModel):
    id: int
    owner_id: int
    name: str
    description: Optional[str] = None
    city: str
    phone: str
    links: Optional[str] = None
    is_visible: bool

    class Config:
        from_attributes = True


class CompanyCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    city: str
    phone: str
    link: Optional[str] = None
    is_visible: bool

    class Config:
        from_attributes = True



class CompanyUpdateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_visible: bool
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True



class CompanyDetails(BaseModel):
    name: str
    description: Optional[str] = None
    city: str

    class Config:
        from_attributes = True


class StatusCompany(BaseModel):
    is_visible: bool

    class Config:
        from_attributes = True