from pydantic import BaseModel
from typing import Union
from enum import Enum

class InvitationSchema(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    company_id: int
    is_accepted: Union[bool, None]

    class Config:
        from_attributes = True


class OwnerActions(str, Enum):
    Send_invitation = "Send_invitation"
    Cancel_invitation = "Cancel_invitation"
    Accept_request = "Accept_request"

    class Config:
        from_attributes = True


class OwnerActionCreate(BaseModel):
    recipient_id: int
    company_id: int
    action: OwnerActions

    class Config:
        from_attributes = True


class UserActions(str, Enum):
    Accept_invitation = "Accept_invitation"
    Deny_invitation = "Deny_invitation"
    Send_request = "Send_request"

    class Config:
      from_attributes = True


class UserActionCreate(BaseModel):
    company_id: int
    action: UserActions

    class Config:
        from_attributes = True



class RequestSchema(BaseModel):
    id: int
    sender_id: int
    company_id: int
    is_accepted:  Union[bool, None]

    class Config:
      from_attributes = True


