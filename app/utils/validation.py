import logging
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.models.model import Invitation, Request, User, Member, Company
from app.schemas.action import OwnerActionCreate, UserActionCreate
from app.services.company import CompanyService
from app.services.user import UserService
from app.utils.exceptions import NotFoundException, AlreadyAdminException, MemberNotAdminException, \
    NoSuchMemberException, PermissionDeniedException, RequestMemberInvitationException


class ActionsValidator:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def owner_action_validation_data(self, action: OwnerActionCreate,
                                           current_user: User,
                                           request_id: Optional[int] = None
                                           ):
        company_service = CompanyService(self.session)
        company = await company_service.get_company_by_id(action.company_id)
        user_service = UserService(self.session)
        user_recipient = await user_service.get_user_by_id(action.recipient_id)
        if not company:
            raise NotFoundException('Company')
        if not user_recipient:
            raise NotFoundException('User')
        if action.recipient_id == current_user.id:
            raise PermissionDeniedException('User')
        if request_id is not None:
            request = await self.session.get(Request, request_id)
            if not request:
                raise NotFoundException('Request')
        return company

    async def check_invitation(self, action, current_user, company):
        stmt = select(Invitation).filter_by(
            sender_id=current_user.id,
            recipient_id=action.recipient_id,
            company_id=company.id,
            is_accepted=None
        )
        result = await self.session.execute(stmt)
        invitation = result.scalars().all()
        if len(invitation) != 0:
            raise RequestMemberInvitationException('invitation')

    async def user_action_validation(self, action: UserActionCreate,
                                     current_user: Optional[int] = None,
                                     invitation_id: Optional[int] = None,
                                     request_id: Optional[int] = None):
        if action.action.Send_request:
            company_service = CompanyService(self.session)
            company = await company_service.get_company_by_id(action.company_id)

            if not company:
                raise NotFoundException('Company')
            if current_user is not None:
                if company.owner_id == current_user.id:
                    raise PermissionDeniedException('User')
            if invitation_id is not None:
                invitation = await self.session.get(Invitation, invitation_id)
                if not invitation:
                    raise NotFoundException('Invitation')
            if request_id is not None:
                request = await self.session.get(Request, request_id)
                if not request:
                    raise NotFoundException('Request')
            return company

    async def check_user_request(self, current_user, company):
        stmt = select(Request).filter_by(
            sender_id=current_user.id, company_id=company.id, is_accepted=None
        )
        result = await self.session.execute(stmt)
        request = result.scalars().all()
        if len(request) != 0:
            raise RequestMemberInvitationException('request')

    async def user_is_not_member(self, recipient_id: int, company_id: int):
        stmt = select(Member).filter_by(user_id=recipient_id, company_id=company_id)
        result = await self.session.execute(stmt)
        member = result.scalars().all()
        if len(member) != 0:
            raise RequestMemberInvitationException('member')
        return True

    async def member_is_not_admin(self, member: Member):
        if member.role == "admin":
            raise AlreadyAdminException()
        return True

    async def member_is_admin(self, member: Member):
        if member.role != "admin":
            raise MemberNotAdminException()
        if member.role == "admin":
            return True

    async def current_user_is_admin(self, current_user: User, company: Company):
        stmt = select(Member).filter_by(user_id=current_user.id, company_id=company.id)
        result = await self.session.execute(stmt)
        member = result.scalar_one()
        if not member:
            raise NoSuchMemberException()
        return await self.member_is_admin(member)
