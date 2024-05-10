import logging
from fastapi import HTTPException
from sqlalchemy import select
from app.models.model import Invitation, Request
from app.schemas.action import OwnerActionCreate, UserActionCreate
from app.services.company import CompanyService
from app.services.user import UserService
from app.utils.exceptions import NotFoundException



class ActionsValidatorService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)


    async def owner_invitation_data(self, action: OwnerActionCreate):
        company_service = CompanyService(self.session)
        company = await company_service.get_company_by_id(action.company_id)
        user_service = UserService(self.session)
        user_recipient = await user_service.get_user_by_id(action.recipient_id)
        if not company:
            raise NotFoundException('Company')
        if not user_recipient:
            raise NotFoundException('User')
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
        if len(invitation) !=0:
            raise HTTPException(status_code=400, detail="Invitation already sent")


    async def user_action_validation(self, action: UserActionCreate):
        if action.action.Send_request:
            company_service = CompanyService(self.session)
            company = await company_service.get_company_by_id(action.company_id)
            if not company:
                raise NotFoundException('Company')
            return company

    async def check_user_request(self, current_user, company):
        stmt = select(Request).filter_by(
            sender_id=current_user.id, company_id=company.id, is_accepted=None
        )
        result = await self.session.execute(stmt)
        request = result.scalars().all()
        if len(request) !=0:
            raise HTTPException(status_code=400, detail="Request already sent")

