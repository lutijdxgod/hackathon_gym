from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.functions.funcs import get_entity_by_field
from app.integrations.yandexgptmanager import get_exercise_advice
from app.models.database import db_helper as db
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.models import Exercise
from app.oauth2 import get_current_user
from app.schemas.users import UserOut

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/exercise/{id}")
async def get_advice_for_exercise(
    id: int = Path(...), db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    exercise_query = select(Exercise).where(Exercise.id == id).options(joinedload(Exercise.equipment))
    query_result = await db.scalars(exercise_query)

    exercise = query_result.first()
    advice = get_exercise_advice(exercise_name=exercise.name, equipment_name=exercise.equipment.name)

    return {"message": advice}
