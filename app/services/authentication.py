import logging
from app.auth.token import create_access_token
from app.schemas.authentication import Token
from app.schemas.schema import UserSignUpRequest, UserSignInRequest
from app.services.user import UserService
from app.utils.exceptions import credentials_exception
from fastapi.security import HTTPAuthorizationCredentials
from app.utils.utils import verify_password
from app.core.config import settings
import jwt



class AuthService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)
    async def authenticate_user(self, user, current_user):
        if not verify_password(user.hashed_password, current_user.hashed_password):
            return False
        access_token = create_access_token(data={"sub": current_user.email})
        return Token(access_token=access_token, token_type="Bearer")


    async def get_user_by_token(self,credentials: HTTPAuthorizationCredentials) -> UserSignInRequest:

                token = credentials.credentials
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
                email = payload.get("sub")
                if email is None:
                    return credentials_exception
                user_service = UserService(self.session)
                user = await user_service.get_user_by_email(email)
                if user is None:
                    return credentials_exception
                return UserSignInRequest.from_orm(user)

