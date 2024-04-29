import os
from datetime import timedelta, datetime
import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = os.environ['ALGORITHM']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']


def create_access_token(data: dict):
    encode = data
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({'exp': expire})
    encoded_jwt = jwt.encode(encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    print('token:',encoded_jwt)
    return encoded_jwt