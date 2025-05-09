from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import db_helper as db
from app.oauth2 import get_current_user
from app.schemas.users import UserOut
from crud.muscle_groups import get_muscle_groups
from app.schemas.muscle_groups import MuscleGroupOut

router = APIRouter(prefix="/muscle_group", tags=["Muscle Group"])


@router.get("/", response_model=list[MuscleGroupOut])
async def get_all_muscle_groups(
    db: Annotated[
        AsyncSession,
        Depends(db.session_getter),
    ],
    user: UserOut = Depends(get_current_user),
):
    result = await get_muscle_groups(session=db)

    return result
