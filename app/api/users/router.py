from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.functions.funcs import get_entity_by_field_nullable, ids_to_string
from app.models.models import Subscription, User, UserInfo
from app.oauth2 import get_current_user
from app.schemas.users import ProfileUser, SubscriptionOut, UserOut
from app.models.database import db_helper as db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/subscriptions", response_model=list[SubscriptionOut])
async def get_users_subscriptions(
    db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    subscriptions = await get_entity_by_field_nullable(
        entity=Subscription, field=Subscription.user_id, value=user.id, session=db
    )

    return ids_to_string(subscriptions)


@router.get("/profile", response_model=ProfileUser)
async def get_users_profile(db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)):
    profile_query = select(User).options(joinedload(User.user_info))
    query_result = await db.execute(profile_query)
    profile: list[User] = query_result.scalars().first()
    print(f"{profile=}")
    info_to_return = user.__dict__
    info_to_return["user_info"] = user.user_info.__dict__

    return info_to_return
