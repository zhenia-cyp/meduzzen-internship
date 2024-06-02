import logging
from sqlalchemy import select, delete
from app.models.model import User, Invitation, Request, Member, Company
from app.schemas.action import UserActionCreate, Role
from app.utils.pagination import Pagination
from app.utils.validation import ActionsValidator
from app.utils.exceptions import NotFoundException


class UserActionsService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def accept_invite(self, action: UserActionCreate, current_user, invitation_id: int):
        validator = ActionsValidator(self.session)
        company = await validator.user_action_validation(action, current_user, invitation_id)
        await validator.user_is_not_member(current_user.id, company.id)
        stmt = select(Invitation).filter_by(id=invitation_id)
        result = await self.session.execute(stmt)
        invitation = result.scalar_one()
        invitation.is_accepted = True
        await self.session.commit()
        await self.session.refresh(invitation)
        member = Member(user_id=current_user.id, role=Role.MEMBER, company_id=company.id)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return invitation

    async def deny_invite(self, action: UserActionCreate, current_user: User, invitation_id: int):
        validator = ActionsValidator(self.session)
        await validator.user_action_validation(action, current_user, invitation_id)
        stmt = select(Invitation).filter_by(id=invitation_id, recipient_id=current_user.id,
                                            company_id=action.company_id,
                                            is_accepted=False)
        result = await self.session.execute(stmt)
        invitation = result.scalar_one()
        invitation.is_accepted = False
        await self.session.commit()
        await self.session.refresh(invitation)
        return invitation

    async def send_request(self, action: UserActionCreate, current_user: User):
        validator = ActionsValidator(self.session)
        company = await validator.user_action_validation(action, current_user)
        await validator.check_user_request(current_user, company)
        request = Request(sender_id=current_user.id, company_id=company.id, is_accepted=False)
        self.session.add(request)
        await self.session.commit()
        await self.session.refresh(request)
        return request

    async def cancel_request(self, request_id: int, current_user):
        stmt = select(Request).filter_by(id=request_id, sender_id=current_user.id)
        result = await self.session.execute(stmt)
        request = result.scalars().all()
        if not request:
            raise NotFoundException()
        stmt = delete(Request).filter_by(id=request_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    async def leave_company(self, user_id: int, action: UserActionCreate, current_user: User):
        stmt = select(Company).filter_by(id=action.company_id)
        result = await self.session.execute(stmt)
        company = result.scalar_one()
        if company.owner_id != current_user.id and user_id == current_user.id:
            stmt = delete(Member).filter_by(user_id=user_id, company_id=company.id)
            await self.session.execute(stmt)
            await self.session.commit()
            return True

    async def get_requests(self, current_user: User, page_params):
        stmt = select(Request).filter_by(sender_id=current_user.id)
        result = await self.session.execute(stmt)
        requests = result.scalars().all()
        pagination = Pagination(User, self.session, page_params, requests)
        return await pagination.get_pagination()

    async def get_invites(self, current_user: User, page_params):
        stmt = select(Invitation).filter_by(recipient_id=current_user.id)
        result = await self.session.execute(stmt)
        requests = result.scalars().all()
        pagination = Pagination(User, self.session, page_params, requests)
        return await pagination.get_pagination()
