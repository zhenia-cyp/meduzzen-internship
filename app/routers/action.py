from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.schemas.action import OwnerActionCreate, InvitationSchema, UserActionCreate, RequestSchema, MemberSchema
from app.schemas.schema import MyResponse
from app.services.authentication import AuthService
from app.services.owner_action import OwnerActionsService
from app.services.user import UserService
from app.services.user_action import UserActionsService
from app.schemas.pagination import PagedResponseSchema, PageParams
from app.utils.exceptions import NoSuchMemberException, CustomTokenExceptionBase


router = APIRouter()
token_auth_scheme = HTTPBearer()


@router.post("/owner/create/invite/", response_model=InvitationSchema)
async def create_owner_action(action: OwnerActionCreate, token: str = Depends(token_auth_scheme),
                              session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    invitation = await owner_actions_service.send_invite(action, current_user)
    return invitation


@router.delete("/owner/cancel/{invitation_id}/", response_model=MyResponse)
async def cancel_user(invitation_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    result = await owner_actions_service.cancel_invite(invitation_id, current_user)
    return MyResponse(status_code="200", message="Cancel invite", result=result)


@router.post("/user/accept/{invitation_id}/", response_model=InvitationSchema)
async def create_user_action(invitation_id: int, action: UserActionCreate,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    invitation = await user_action_service.accept_invite(action, current_user, invitation_id)
    return invitation


@router.post("/user/deny/{invitation_id}/", response_model=InvitationSchema)
async def create_user_action(invitation_id: int, action: UserActionCreate,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    invitation = await user_action_service.deny_invite(action, current_user, invitation_id)
    return invitation


@router.post("/user/send/request/", response_model=RequestSchema)
async def create_user_action(action: UserActionCreate,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    request = await user_action_service.send_request(action, current_user)
    return request


@router.post("/user/cancel/{request_id}/", response_model=MyResponse[RequestSchema])
async def create_user_action(request_id: int,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    result = await user_action_service.cancel_request(request_id, current_user)
    return MyResponse(status_code="200", message="Cancel request", result=result)


@router.post("/owner/accept/{request_id}/", response_model=RequestSchema)
async def owner_accept_request(request_id: int, action: OwnerActionCreate,
                               session: AsyncSession = Depends(get_async_session),
                               token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    request = await owner_actions_service.accept_request(action, current_user, request_id)
    return request


@router.post("/owner/deny/{request_id}/", response_model=RequestSchema)
async def owner_deny_request(request_id: int, action: OwnerActionCreate,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    request = await owner_actions_service.deny_request(action, current_user, request_id)
    return request


@router.post("/user/leave/{user_id}/", response_model=MyResponse)
async def user_leave_company(user_id: int, action: UserActionCreate,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_action_service = UserActionsService(session)
    result = await user_action_service.leave_company(user_id, action, current_user)
    if result:
        return MyResponse(status_code="200", message="Leave company", result=result)
    return MyResponse(status_code="200", message="Leave company", result=result)


@router.get("/get/all/requests/", response_model=PagedResponseSchema[RequestSchema])
async def all_requests(session: AsyncSession = Depends(get_async_session),
                       token: str = Depends(token_auth_scheme),
                       page_params: PageParams = Depends(PageParams)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_actions_service = UserActionsService(session)
    requests = await user_actions_service.get_requests(current_user, page_params)
    return requests


@router.get("/user/get/all/invites/", response_model=PagedResponseSchema[RequestSchema])
async def all_invites_by_user(session: AsyncSession = Depends(get_async_session),
                              token: str = Depends(token_auth_scheme),
                              page_params: PageParams = Depends(PageParams)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    user_actions_service = UserActionsService(session)
    invites = await user_actions_service.get_invites(current_user, page_params)
    return invites


@router.get("/owner/get/invited/users/", response_model=PagedResponseSchema[InvitationSchema])
async def all_requests_by_user(session: AsyncSession = Depends(get_async_session),
                               token: str = Depends(token_auth_scheme),
                               page_params: PageParams = Depends(PageParams)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    invited_users = await owner_actions_service.get_invited_users(current_user, page_params)
    return invited_users


@router.get("/owner/get/join/requests/", response_model=PagedResponseSchema[RequestSchema])
async def join_requests(session: AsyncSession = Depends(get_async_session),
                        token: str = Depends(token_auth_scheme),
                        page_params: PageParams = Depends(PageParams)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    requests = await owner_actions_service.get_join_requests(current_user, page_params)
    return requests


@router.get("/owner/company/users/{company_id}/", response_model=PagedResponseSchema[MemberSchema])
async def company_users(company_id: int, session: AsyncSession = Depends(get_async_session),
                        token: str = Depends(token_auth_scheme),
                        page_params: PageParams = Depends(PageParams)):
    auth_service = AuthService(session)
    try:
        user = await auth_service.get_user_by_token(token, session)
    except CustomTokenExceptionBase as e:
        raise e
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    members = await owner_actions_service.company_users(company_id, current_user, page_params)
    return members


@router.post("/create/admin/{user_id}/", response_model=MemberSchema)
async def owner_create_admin(user_id: int, action: OwnerActionCreate,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    member = await owner_actions_service.add_admin_role(user_id, action, current_user)
    return member


@router.post("/delete/admin/role/{user_id}/", response_model=MyResponse)
async def owner_delete_admin(user_id: int, action: OwnerActionCreate,
                             session: AsyncSession = Depends(get_async_session),
                             token: str = Depends(token_auth_scheme)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    result = await owner_actions_service.remove_admin_role(user_id, action, current_user)
    if not result:
        NoSuchMemberException()
    return MyResponse(status_code="200", message="Delete admin role", result=result)


@router.post("/get/company/admins/{company_id}/", response_model=PagedResponseSchema[MemberSchema])
async def owner_get_admins(company_id: int, session: AsyncSession = Depends(get_async_session),
                           token: str = Depends(token_auth_scheme),
                           page_params: PageParams = Depends(PageParams)):
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_token(token, session)
    user_service = UserService(session)
    user = await user_service.get_user_by_email(user.email)
    current_user = await user_service.get_user_by_id(user.id)
    owner_actions_service = OwnerActionsService(session)
    admins = await owner_actions_service.get_admins(company_id, current_user, page_params)
    return admins
