from passlib.context import CryptContext


password_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_hash_password(password):
    return password_crypt_context.hash(password)