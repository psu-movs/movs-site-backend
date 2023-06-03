from datetime import timedelta, datetime
from os import environ
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
HASH_ALGORITH = "HS256"


def hash_value(value: str) -> str:
    return pwd_context.hash(value)


def verify_hashed_value(value: str, hashed_value: str) -> bool:
    return pwd_context.verify(value, hashed_value)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, environ["OPENSSL_SECRET_KEY"], algorithm=HASH_ALGORITH)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        decoded_token_data = jwt.decode(token, environ["OPENSSL_SECRET_KEY"], algorithms=[HASH_ALGORITH])
    except JWTError:
        raise

    email = decoded_token_data.get("sub")

    user = await User.find_one(User.email == email)
    if not user:
        raise

    return user

