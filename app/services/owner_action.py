import logging
from http.client import HTTPException
from sqlalchemy import select, delete
from app.models.model import Invitation, User, Request
from app.schemas.action import OwnerActionCreate
from app.services.validation import ActionsValidatorService
from app.utils.exceptions import NotFoundException


class OwnerActionsService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def send_invite(self, action: OwnerActionCreate, current_user: User):
        validator = ActionsValidatorService(self.session)
        company = await validator.owner_invitation_data(action)
        if action.recipient_id == current_user.id:
             raise HTTPException(status_code=400, detail="user is owner of a company")

        await validator.check_invitation(action, current_user, company)
        invitation = Invitation(sender_id=current_user.id,recipient_id=action.recipient_id,company_id=company.id,is_accepted=None)
        self.session.add(invitation)
        await self.session.commit()
        await self.session.refresh(invitation)
        return invitation


    async def cancel_invite(self,invitation_id: int, current_user: User):
          stmt = select(Invitation).filter_by(id=invitation_id, sender_id=current_user.id)
          result = await self.session.execute(stmt)
          invitation = result.scalars().all()
          if not invitation:
              raise NotFoundException()
          stmt = delete(Invitation).filter_by(id=invitation_id)
          await self.session.execute(stmt)
          await self.session.commit()
          return True


    async def accept_request(self, action: OwnerActionCreate):
        validator = ActionsValidatorService(self.session)
        company = await validator.owner_invitation_data(action)
        stmt = select(Request).filter_by(
            sender_id=action.recipient_id, company_id=company.id, is_accepted=None
        )
        result = await self.session.execute(stmt)
        request = result.scalar_one()
        request.is_accepted = True
        self.session.add(request)
        await self.session.commit()
        await self.session.refresh(request)
        return request
