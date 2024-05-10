from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.models.model import Invitation, Request
from app.schemas.action import OwnerActionCreate, InvitationSchema, UserActionCreate, RequestSchema
from app.schemas.schema import MyResponse
from app.services.authentication import AuthService
from app.services.owner_action import OwnerActionsService
from app.services.user import UserService
from sqlalchemy import select
from typing import List

from app.services.user_action import UserActionsService

router = APIRouter()
token_auth_scheme = HTTPBearer()


@router.post("/owner/create/invite/", response_model=InvitationSchema)
async def create_owner_action(action: OwnerActionCreate, token: str = Depends(token_auth_scheme), session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    invitation = await owner_actions_service.send_invite(action, current_user)
    return invitation



@router.delete("/owner/cancel/invite/{user_id}/", response_model=MyResponse)
async def cancel_user(invitation_id: int, session: AsyncSession = Depends(get_async_session), token: str = Depends(token_auth_scheme)):
     auth_service = AuthService(session)
     user = await auth_service.get_user_by_token(token, session)
     user_service = UserService(session)
     user = await user_service.get_user_by_email(user.email)
     current_user = await user_service.get_user_by_id(user.id)
     owner_actions_service = OwnerActionsService(session)
     result = await owner_actions_service.cancel_invite(invitation_id, current_user)
     return MyResponse(status_code="200",message="Cancel invite",result=result)



@router.post("/user/accept/invite/", response_model=InvitationSchema)
async def create_user_action(action: UserActionCreate, session: AsyncSession = Depends(get_async_session), token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    invitation = await user_action_service.accept_invite(action, current_user)
    return invitation


@router.post("/user/deny/invite/", response_model=InvitationSchema)
async def create_user_action(action: UserActionCreate, session: AsyncSession = Depends(get_async_session), token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    invitation = await user_action_service.deny_invite(action, current_user)
    return invitation


@router.post("/user/send/request/", response_model=RequestSchema)
async def create_user_action(action: UserActionCreate, session: AsyncSession = Depends(get_async_session), token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    request = await user_action_service.send_request(action, current_user)
    return request


@router.post("/user/cancel/request/{request_id}/", response_model=MyResponse[RequestSchema])
async def create_user_action(request_id: int, session: AsyncSession = Depends(get_async_session), token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    result = await user_action_service.cancel_request(request_id, current_user)
    return MyResponse(status_code="200",message="Cancel request",result=result)



@router.post("/owner/accept/request/", response_model=RequestSchema)
async def owner_accept_request(action: OwnerActionCreate, session: AsyncSession = Depends(get_async_session), token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    await auth_service.get_user_by_token(token, session)
    owner_actions_service = OwnerActionsService(session)
    request = await owner_actions_service.accept_request(action)
    return request



@router.get("/all/invites/",response_model=List[InvitationSchema])
async def all_invitations(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Invitation)
    result = await session.execute(stmt)
    invitations = result.scalars().all()
    print('invite:', invitations)
    return [InvitationSchema.from_orm(invite) for invite in invitations]


@router.get("/all/requests/",response_model=List[RequestSchema])
async def all_invitations(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Request)
    result = await session.execute(stmt)
    requests = result.scalars().all()
    print('requests:', requests)
    return [RequestSchema.from_orm(rq) for rq in requests]