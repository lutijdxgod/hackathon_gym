from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from app.models.database import db_helper as db
from app.oauth2 import get_current_user
from app.schemas.exercises import (
    ExerciseByEquipment,
    ExerciseByMuscleGroupFiltered,
    ExerciseInList,
    ExerciseInfo,
    ExercisesList,
)
from app.api.functions.funcs import (
    get_entity_by_multiple_fields_nullable,
    get_entity_by_field,
)
from app.models.models import Exercise, TrainingLevel
from app.schemas.users import UserOut

router = APIRouter(prefix="/exercise", tags=["Exercises"])


@router.get("/", response_model=list[ExerciseInList])
async def get_exercises_by_muscle_group(
    db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    pass


@router.get("/{id}", response_model=ExerciseInfo)
async def get_exercise_info(
    id: int = Path(...), db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    exercise_query = (
        select(Exercise)
        .where(Exercise.id == id)
        .options(selectinload(Exercise.exercise_media))
    )
    query_result = await db.scalars(exercise_query)
    result = query_result.first()
    return result


@router.get("/muscle_group/{id}", response_model=ExercisesList)
async def get_exercises_by_muscle_group(
    id: int = Path(...),
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    beginner_exercises = await get_entity_by_multiple_fields_nullable(
        entity=Exercise,
        fields=[Exercise.muscle_group_id == id, Exercise.difficulty == TrainingLevel.beginner],
        session=db,
    )
    intermediate_exercises = await get_entity_by_multiple_fields_nullable(
        entity=Exercise,
        fields=[Exercise.muscle_group_id == id, Exercise.difficulty == TrainingLevel.intermediate],
        session=db,
    )
    advanced_exercises = await get_entity_by_multiple_fields_nullable(
        entity=Exercise,
        fields=[Exercise.muscle_group_id == id, Exercise.difficulty == TrainingLevel.advanced],
        session=db,
    )

    return {
        "beginner_exercises": beginner_exercises,
        "intermediate_exercises": intermediate_exercises,
        "advanced_exercises": advanced_exercises,
    }


@router.get("/muscle_group_filtered/{id}", response_model=list[ExerciseByMuscleGroupFiltered])
async def get_exercises_by_muscle_group(
    id: int = Path(...),
    level: TrainingLevel | None = Query(default=None),
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    filters = [Exercise.muscle_group_id == id]
    if level is not None:
        filters.append(Exercise.difficulty == level)

    result = await get_entity_by_multiple_fields_nullable(
        entity=Exercise,
        fields=filters,
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
