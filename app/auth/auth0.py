import jwt
from jwt import PyJWKClient
from app.core.config import settings
from app.schemas.schema import UserSignUpRequest
from app.services.user import UserService
from app.utils.exceptions import CredentialsException
import secrets
from app.utils.utils import get_hash_password

async def payload_auth(token, session):
    url = f"https://{settings.DOMAIN}/.well-known/jwks.json"
    jwks_client = PyJWKClient(url)
    signing_key = jwks_client.get_signing_key_from_jwt(token).key
    payload = jwt.decode(token, signing_key, algorithms=[settings.ALGORITHM_RS], audience=settings.AUDIENCE)
    email = payload.get("email")
    if email is None:
        raise CredentialsException()
    user_service = UserService(session)
    user = await user_service.get_user_by_email(email)
    if user is None:
        added_user = UserSignUpRequest(email=email, password=get_hash_password(secrets.token_urlsafe(15)),
              firstname="string", lastname="string", is_active=True, is_superuser=False)
        user = await user_service.add_user(added_user)
        return user
    return user

