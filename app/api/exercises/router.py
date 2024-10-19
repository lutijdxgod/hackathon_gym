from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import db_helper as db
from app.schemas.exercises import ExerciseByMuscleGroup, ExerciseByEquipment
from app.api.functions.funcs import get_entity_by_field
from app.models.models import Exercise

router = APIRouter(prefix="/exercise", tags=["Exercises"])


@router.get("/muscle_group/{id}", response_model=list[ExerciseByMuscleGroup])
async def get_exercises_by_muscle_group(
    id: int = Path(...),
    db: AsyncSession = Depends(db.session_getter),
):
    result = await get_entity_by_field(
        entity=Exercise,
        field=Exercise.muscle_group_id,
        value=id,
        session=db,
    )

    return result


@router.get("/equipment/{id}", response_model=list[ExerciseByEquipment])
async def get_exercises_by_equipment_id(
    id: int = Path(...),
    db: AsyncSession = Depends(db.session_getter),
):
    result = await get_entity_by_field(
            entity=Exercise, field=Exercise.equipment_id, value=id, session=db
        )
    
    return result