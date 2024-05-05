import logging
from app.auth.auth0 import payload_auth
from app.auth.token import create_access_token, payload
from app.schemas.authentication import Token
from app.schemas.schema import UserDetails
from fastapi.security import HTTPAuthorizationCredentials
from app.utils.exceptions import TokenDecodingError, TokenExpiredException
from app.utils.utils import verify_password



class AuthService:
    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(__name__)


    async def authenticate_user(self, user, current_user):
        if not verify_password(user.hashed_password, current_user.hashed_password):
            return False
        access_token = create_access_token(data={"sub": current_user.email})
        return Token(access_token=access_token, token_type="Bearer")


    async def get_user_by_token(self,credentials: HTTPAuthorizationCredentials,session) -> UserDetails:
        token = credentials.credentials
        try:
            user = await payload(token, session)
            return UserDetails.from_orm(user)
        except Exception as e:
            self.logger.error(f" {str(e)}")
        try:
            user = await payload_auth(token, session)
            return UserDetails.from_orm(user)
        except Exception as e:
                self.logger.error(f" {str(e)}")
                raise TokenDecodingError()


