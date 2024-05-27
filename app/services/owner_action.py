import logging
from sqlalchemy import select, delete
from app.models.model import Invitation, User, Request, Member, Company
from app.schemas.action import OwnerActionCreate, UserActionCreate, Role
from app.services.company import CompanyService
from app.utils.pagination import Pagination
from app.utils.permissions import ActionPermission
from app.utils.validation import ActionsValidator
from app.utils.exceptions import NotFoundException


class OwnerActionsService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def add_member(self, action: OwnerActionCreate, company: Company) -> Member:
        validator = ActionsValidator(self.session)
        await validator.user_is_not_member(action.recipient_id, company.id)
        member = Member(user_id=action.recipient_id, role=Role.Member, company_id=company.id)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def send_invite(self, action: OwnerActionCreate, current_user: User):
        action_permission = ActionPermission()
        validator = ActionsValidator(self.session)
        company = await validator.owner_action_validation_data(action, current_user)
        if await action_permission.is_owner(company, current_user):
            await validator.check_invitation(action, current_user, company)
            await validator.user_is_not_member(action.recipient_id, company.id)
            invitation = Invitation(sender_id=current_user.id, recipient_id=action.recipient_id, company_id=company.id,
                                    is_accepted=False)
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
        action_permission = ActionPermission()
        validator = ActionsValidator(self.session)
        company = await validator.owner_action_validation_data(action, current_user)
        if (await validator.current_user_is_admin(current_user, company)
                or action_permission.is_owner(company.id, current_user)):
            await validator.user_is_not_member(action.recipient_id, company.id)
            stmt = select(Request).filter_by(id=request_id, sender_id=action.recipient_id,
                                             company_id=company.id, is_accepted=False)
            result = await self.session.execute(stmt)
            request = result.scalar_one()
            request.is_accepted = True
            self.session.add(request)
            await self.session.commit()
            await self.session.refresh(request)
            await self.add_member(action, company)
            return request

    async def deny_request(self, action: OwnerActionCreate, current_user, request_id: int):
        action_permission = ActionPermission()
        validator = ActionsValidator(self.session)
        company = await validator.owner_action_validation_data(action, current_user, request_id)
        if (await validator.current_user_is_admin(current_user, company)
                or action_permission.is_owner(company.id, current_user)):
            stmt = select(Request).filter_by(id=request_id)
            result = await self.session.execute(stmt)
            request = result.scalar_one()
            request.is_accepted = False
            await self.session.commit()
            await self.session.refresh(request)
            return request

    async def delete_member(self, user_id: int, action: UserActionCreate, current_user: User):
        action_permission = ActionPermission()
        validator = ActionsValidator(self.session)
        stmt = select(Company).filter_by(id=action.company_id)
        result = await self.session.execute(stmt)
        company = result.scalar_one()
        if await validator.current_user_is_admin(current_user, company) or action_permission.is_owner(company.id, current_user):
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

    async def add_admin_role(self, user_id: int, action: OwnerActionCreate, current_user: User):
        action_permission = ActionPermission()
        validator = ActionsValidator(self.session)
        company = await validator.owner_action_validation_data(action, current_user)
        await action_permission.is_owner(company, current_user)
        stmt = select(Member).filter_by(user_id=user_id, company_id=company.id)
        result = await self.session.execute(stmt)
        member = result.scalar_one()
        await validator.member_is_not_admin(member)
        member.role = Role.Admin
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def remove_admin_role(self, user_id: int, action: OwnerActionCreate, current_user: User):
        action_permission = ActionPermission()
        validator = ActionsValidator(self.session)
        company = await validator.owner_action_validation_data(action, current_user)
        await action_permission.is_owner(company, current_user)
        stmt = select(Member).filter_by(user_id=user_id, company_id=company.id)
        result = await self.session.execute(stmt)
        member = result.scalar_one()
        await validator.member_is_admin(member)
        await self.session.delete(member)
        await self.session.commit()
        return True

    async def get_admins(self, company_id: int, current_user: User, page_params):
        action_permission = ActionPermission()
        company_service = CompanyService(self.session)
        company = await company_service.get_company_by_id(company_id)
        await action_permission.is_owner(company, current_user)
        stmt = select(Member). \
            join(User, User.id == Member.user_id). \
            filter(Member.role == 'admin', Member.company_id == company_id)
        result = await self.session.execute(stmt)
        admins = result.scalars().all()
        pagination = Pagination(User, self.session, page_params, admins)
        return await pagination.get_pagination()
