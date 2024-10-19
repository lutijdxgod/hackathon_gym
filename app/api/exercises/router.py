from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import db_helper as db
from app.schemas.exercises import ExerciseOut
from app.api.functions.funcs import get_entity_by_field
from app.models.models import Exercise

router = APIRouter(prefix="/exercise", tags=["Exercises"])


@router.get("/", response_model=list[ExerciseOut])
async def get_exercises_by_muscle_group(
    muscle_group_id: int = Query(...),
    db: AsyncSession = Depends(db.session_getter),
):
    result = await get_entity_by_field(
        entity=Exercise,
        field=Exercise.muscle_group_id,
        value=muscle_group_id,
        session=db,
    )

    return result
