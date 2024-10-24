from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import db_helper as db
from app.oauth2 import get_current_user
from app.schemas.exercises import ExerciseByMuscleGroup, ExerciseByEquipment
from app.api.functions.funcs import get_entity_by_multiple_fields_nullable, get_entity_by_field
from app.models.models import Exercise, TrainingLevel
from app.schemas.users import UserOut

router = APIRouter(prefix="/exercise", tags=["Exercises"])


@router.get("/muscle_group/{id}", response_model=list[ExerciseByMuscleGroup])
async def get_exercises_by_muscle_group(
    id: int = Path(...),
    level: TrainingLevel = Query(...),
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    result = await get_entity_by_multiple_fields_nullable(
        entity=Exercise,
        fields=[Exercise.muscle_group_id == id, Exercise.difficulty == level],
        session=db,
    )

    return result


@router.get("/equipment/{id}", response_model=list[ExerciseByEquipment])
async def get_exercises_by_equipment_id(
    id: int = Path(...),
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    result = await get_entity_by_field(entity=Exercise, field=Exercise.equipment_id, value=id, session=db)

    return result
