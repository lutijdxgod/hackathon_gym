from jose import JWTError, jwt
from fastapi import Depends, Response, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import db_helper as db
from .models import models
from app.schemas.users import Token, TokenData
from .config import settings
from sqlalchemy import select
from sqlalchemy.orm import joinedload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.auth.secret_key
ALGORITHM = settings.auth.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(payload)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(user_id=str(id))

    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(token: Token = Depends(oauth2_scheme), db: AsyncSession = Depends(db.session_getter)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user_query = (
        select(models.User).where(models.User.id == int(token.user_id)).options(joinedload(models.User.user_info))
    )
    query_result = await db.scalars(user_query)
    user = query_result.first()

    return user


def plain_get_current_user(token: Token = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    return Response(status_code=status.HTTP_200_OK)
