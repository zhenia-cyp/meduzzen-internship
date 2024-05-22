import logging
from sqlalchemy import select, delete
from app.models.model import Invitation, User, Request, Member, Company
from app.schemas.action import OwnerActionCreate, UserActionCreate
from app.utils.pagination import Pagination
from app.utils.validation import ActionsValidator
from app.utils.exceptions import NotFoundException


class OwnerActionsService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def add_member(self, action: OwnerActionCreate, company: Company) -> Member:
        validator = ActionsValidator(self.session)
        await validator.user_is_not_member(action.recipient_id, company.id)
        member = Member(user_id=action.recipient_id, role="member", company_id=company.id)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def send_invite(self, action: OwnerActionCreate, current_user: User):
        validator = ActionsValidator(self.session)
        company = await validator.owner_action_validation_data(action, current_user)
        await validator.check_invitation(action, current_user, company)
        await validator.user_is_not_member(action.recipient_id, company.id)
        invitation = Invitation(sender_id=current_user.id, recipient_id=action.recipient_id, company_id=company.id,
                                is_accepted=None)
        self.session.add(invitation)
        await self.session.commit()
        await self.session.refresh(invitation)
        return invitation

    async def cancel_invite(self, invitation_id: int, current_user: User):
        stmt = select(Invitation).filter_by(id=invitation_id, sender_id=current_user.id)
        result = await self.session.execute(stmt)
        invitation = result.scalars().all()
        if not invitation:
            raise NotFoundException()
        stmt = delete(Invitation).filter_by(id=invitation_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    async def accept_request(self, action: OwnerActionCreate, current_user: User,  request_id: int):
        validator = ActionsValidator(self.session)
        company = await validator.owner_action_validation_data(action, current_user)
        await validator.user_is_not_member(action.recipient_id, company.id)
        stmt = select(Request).filter_by(id=request_id, sender_id=action.recipient_id,
                                         company_id=company.id, is_accepted=None)
        result = await self.session.execute(stmt)
        request = result.scalar_one()
        request.is_accepted = True
        self.session.add(request)
        await self.session.commit()
        await self.session.refresh(request)
        await self.add_member(action, company)
        return request

    async def deny_request(self, action: UserActionCreate, request_id: int, current_user, invitation_id: int):
        validator = ActionsValidator(self.session)
        await validator.user_action_validation(action, current_user, invitation_id, request_id)
        stmt = select(Request).filter_by(id=request_id)
        result = await self.session.execute(stmt)
        request = result.scalar_one()
        request.is_accepted = False
        await self.session.commit()
        await self.session.refresh(request)
        return request

    async def delete_member(self, user_id: int, action: UserActionCreate, current_user: User):
        stmt = select(Company).filter_by(id=action.company_id)
        result = await self.session.execute(stmt)
        company = result.scalar_one()
        if company.owner_id == current_user.id and user_id != current_user.id:
            stmt = delete(Member).filter_by(user_id=user_id, company_id=company.id)
            await self.session.execute(stmt)
            await self.session.commit()
            return True

    async def get_invited_users(self, current_user: User, page_params):
        stmt = select(Invitation). \
            join(Company, Company.id == Invitation.company_id). \
            filter(Company.owner_id == current_user.id).filter(Invitation.is_accepted == True)
        result = await self.session.execute(stmt)
        invited_users = result.scalars().all()
        pagination = Pagination(User, self.session, page_params, invited_users)
        return await pagination.get_pagination()

    async def get_join_requests(self, current_user: User, page_params):
        stmt = select(Request).\
            join(Company, Company.id == Request.company_id).\
            filter(Company.owner_id == current_user.id)
        result = await self.session.execute(stmt)
        requests = result.scalars().all()
        pagination = Pagination(User, self.session, page_params, requests)
        return await pagination.get_pagination()

    async def company_users(self, company_id: int, current_user: User, page_params):
        stmt = select(Company).filter_by(id=company_id)
        result = await self.session.execute(stmt)
        company = result.scalar_one()
        if company.owner_id == current_user.id:
            stmt = select(Member). \
                join(User, User.id == Member.user_id). \
                filter(Member.company_id == company_id)
            result = await self.session.execute(stmt)
            members = result.scalars().all()
            pagination = Pagination(User, self.session, page_params, members)
            return await pagination.get_pagination()
