from app.models.model import User, Company
from app.utils.exceptions import PermissionDeniedException


class ActionPermission:
    def __init__(self):
        self.permission_error = PermissionDeniedException()

    async def is_owner(self, company: Company, current_user: User) -> bool:
        if current_user.id != company.owner_id:
            raise self.permission_error
        return True
