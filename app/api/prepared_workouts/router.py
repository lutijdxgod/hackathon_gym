from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import (
    Exercise,
    PreparedWorkout,
    PreparedWorkoutsExercises,
)
from app.oauth2 import get_current_user
from app.schemas.prepared_workout import (
    MuscleGroupIds,
    PreparedWorkoutByMuscleGroups,
    PreparedWorkoutOut,
)
from app.schemas.users import UserOut
from app.models.database import db_helper as db
from crud.prepared_workouts import (
    get_prepared_workout_by_id,
    get_prepared_workout_by_muscle_group_ids,
)

router = APIRouter(prefix="/prepared_workouts", tags=["Prepared Workouts"])


@router.get(
    "/muscle_groups", response_model=list[PreparedWorkoutByMuscleGroups]
)
async def get_workout_by_muscle_group_ids(
    muscle_groups: MuscleGroupIds = Body(...),
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    workouts = await get_prepared_workout_by_muscle_group_ids(
        muscle_group_ids=muscle_groups.ids, session=db
    )
    return workouts


@router.get("/{workout_id}", response_model=PreparedWorkoutOut)
async def get_workout_by_id(
    workout_id: int,
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    workout = await get_prepared_workout_by_id(
        workout_id=workout_id, session=db
    )
    return workout
