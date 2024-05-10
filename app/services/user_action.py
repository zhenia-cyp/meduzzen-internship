import logging
from http.client import HTTPException
from sqlalchemy import select, delete
from app.models.model import User, Invitation, Request
from app.schemas.action import UserActionCreate, InvitationSchema
from app.services.validation import ActionsValidatorService
from app.utils.exceptions import NotFoundException


class UserActionsService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def accept_invite(self, action: UserActionCreate, current_user: User):
        validator = ActionsValidatorService(self.session)
        await validator.user_action_validation(action)
        stmt = select(Invitation).filter_by(recipient_id=current_user.id,company_id=action.company_id,is_accepted=None)
        result = await self.session.execute(stmt)
        invitation = result.scalar_one()

        if not invitation:
            raise HTTPException(status_code=400, detail="User has not been invited")
        invitation.is_accepted = True
        await self.session.commit()
        await self.session.refresh(invitation)
        return invitation

    async def deny_invite(self, action: UserActionCreate, current_user: User):
        validator = ActionsValidatorService(self.session)
        await validator.user_action_validation(action)
        stmt = select(Invitation).filter_by(recipient_id=current_user.id, company_id=action.company_id,
                                            is_accepted=None)
        result = await self.session.execute(stmt)
        invitation = result.scalar_one()
        if not invitation:
            raise HTTPException(status_code=400, detail="User has not been invited")
        invitation.is_accepted = False
        await self.session.commit()
        await self.session.refresh(invitation)
        return invitation


    async def send_request(self, action: UserActionCreate, current_user: User):
        validator = ActionsValidatorService(self.session)
        company = await validator.user_action_validation(action)
        if company.owner_id == current_user.id:
            raise HTTPException(status_code=400, detail="User is owner of a company")

        await validator.check_user_request(current_user,company)
        request = Request(sender_id=current_user.id, company_id=company.id, is_accepted=None)
        self.session.add(request)
        await self.session.commit()
        await self.session.refresh(request)
        return request


    async def cancel_request(self,request_id: int, current_user):
          stmt = select(Request).filter_by(id=request_id, sender_id=current_user.id)
          result = await self.session.execute(stmt)
          request = result.scalars().all()
          if not request:
              raise NotFoundException()
          stmt = delete(Request).filter_by(id=request_id)
          await self.session.execute(stmt)
          await self.session.commit()
          return True
