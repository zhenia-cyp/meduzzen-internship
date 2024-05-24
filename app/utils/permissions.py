from fastapi import HTTPException
from app.models.model import User, Company, Member
from sqlalchemy import select

class ActionPermission:
    def __init__(self):
        self.permission_error = HTTPException(status_code=403, detail="Not enough permissions")

    async def is_owner(self, company: Company, current_user: User) -> bool:
        if current_user.id != company.owner_id:
            raise self.permission_error
        return True
