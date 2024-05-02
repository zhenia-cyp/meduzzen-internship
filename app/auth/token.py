from datetime import timedelta, datetime
import jwt
from app.core.config import settings
from app.services.user import UserService
from app.utils.exceptions import CredentialsException, TokenExpiredException


def create_access_token(data: dict):
    encode = data
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({'exp': expire})
    encoded_jwt = jwt.encode(encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def payload(token, session):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    exp = payload.get('exp')
    if exp is not None and datetime.utcfromtimestamp(exp) < datetime.utcnow():
        raise TokenExpiredException()
    email = payload.get("sub")
    if email is None:
        return CredentialsException()
    user_service = UserService(session)
    user = await user_service.get_user_by_email(email)
    if user is None:
        return CredentialsException()
    return user