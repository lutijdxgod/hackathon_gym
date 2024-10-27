from fastapi import APIRouter, Depends, Query, Request, Response, status, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app import oauth2
from app.api.auth.utils import hash_password, verify_hashes
from app.schemas.users import UserCreate, UserLogin, UserOut, UserRegisterCheckCode, Token
from app.config import settings
from app.models.database import db_helper as db
from app.models.models import UserVerification, User
from . import service
from app.api import exceptions

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def create_user(user: UserCreate, db: AsyncSession = Depends(db.session_getter)):
    user_verification_query = select(UserVerification).where(UserVerification.phone_number == user.phone_number)
    query_result = await db.scalars(user_verification_query)
    user_verification = query_result.first()

    if user_verification is not None:
        if user_verification.user_id is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Пользователь с телефоном +7{user.phone_number} уже существует.",
            )
        else:
            verification_code = service.get_verification_code(user.phone_number)
            update_query = (
                update(UserVerification)
                .where(UserVerification.phone_number == user.phone_number)
                .values(verification_code=verification_code)
            )
            await db.execute(update_query)
            await db.commit()

            return Response(status_code=status.HTTP_200_OK)
    else:
        verification_code = service.get_verification_code(phone_number=user.phone_number)

        new_user = UserVerification(**{"phone_number": user.phone_number, "verification_code": verification_code})
        db.add(new_user)
        await db.commit()
        return Response(status_code=status.HTTP_201_CREATED)


@router.post("/check_verification_code_register", response_model=Token)
async def check_verification_code_register(
    credentials: UserRegisterCheckCode,
    db: AsyncSession = Depends(db.session_getter),
):
    verification_code_query = select(UserVerification).where(
        UserVerification.phone_number == credentials.phone_number,
        UserVerification.verification_code == credentials.verification_code,
    )
    query_result = await db.scalars(verification_code_query)

    verification_code_raw = query_result.first()
    if verification_code_raw is not None:
        if verification_code_raw.user_id is None:
            new_user = User(
                **{
                    "name": credentials.name,
                    "surname": credentials.surname,
                    "phone_number": credentials.phone_number,
                    "password": hash_password(credentials.password),
                }
            )
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            user_id = new_user.id
            update_query = (
                update(UserVerification)
                .where(UserVerification.phone_number == new_user.phone_number)
                .values(user_id=user_id, verification_code=None)
            )
            await db.execute(update_query)
            await db.commit()

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Аккаунт с номером +7{credentials.phone_number} уже существует.",
            )
    else:
        raise exceptions.wrong_credentials
    access_token = oauth2.create_access_token(data={"user_id": new_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(new_user.id),
    }


@router.post("/login", response_model=Token)
async def user_login(user_credentials: UserLogin, db: AsyncSession = Depends(db.session_getter)):
    user_query = select(User).where(User.phone_number == user_credentials.phone_number)
    query_result = await db.scalars(user_query)
    user = query_result.first()

    if (user is None) or (not verify_hashes(user_credentials.password, user.password)):
        raise exceptions.wrong_credentials

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
    }


@router.get("/validate_user")
async def validate_user(user: UserOut = Depends(oauth2.get_current_user)):
    return Response(status_code=status.HTTP_200_OK)
