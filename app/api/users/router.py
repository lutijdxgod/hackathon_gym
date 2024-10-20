from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.functions.funcs import get_entity_by_field_nullable, ids_to_string
from app.models.models import Subscription
from app.oauth2 import get_current_user
from app.schemas.users import SubscriptionOut, UserOut
from app.models.database import db_helper as db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/subscriptions", response_model=list[SubscriptionOut])
async def get_users_subscriptions(
    db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    subscriptions = await get_entity_by_field_nullable(
        entity=Subscription, field=Subscription.user_id, value=user.id, session=db
    )

    # TODO: объяснить Темику чо это за функция такая
    return ids_to_string(subscriptions)
