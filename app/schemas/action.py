from pydantic import BaseModel
from typing import Union
from enum import StrEnum


class InvitationSchema(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    company_id: int
    is_accepted: Union[bool, None]

    class Config:
        from_attributes = True


class OwnerActions(StrEnum):
    Send_invitation = "Send_invitation"
    Cancel_invitation = "Cancel_invitation"
    Send_request = "Send_request"
    Accept_request = "Accept_request"
    Deny_request = "Deny_request"
    Delete_member = "Delete_member"
    Add_admin = "Add_admin"
    Remove_admin = "Remove_admin"


class OwnerActionCreate(BaseModel):
    recipient_id: int
    company_id: int
    action: OwnerActions

    class Config:
        from_attributes = True


class UserActions(StrEnum):
    Accept_invitation = "Accept_invitation"
    Deny_invitation = "Deny_invitation"
    Send_request = "Send_request"
    Deny_request = "Deny_request"
    Leave_company = "Leave_company"


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


class MemberSchema(BaseModel):
    id: int
    user_id: int
    role: str
    company_id: int

    class Config:
        from_attributes = True
