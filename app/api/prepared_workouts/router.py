from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import PreparedWorkout, PreparedWorkoutsExercises
from app.oauth2 import get_current_user
from app.schemas.prepared_workout import PreparedWorkoutOut
from app.schemas.users import UserOut
from app.models.database import db_helper as db
from crud.prepared_workouts import get_prepared_workout_by_id

router = APIRouter(prefix="/prepared_workouts", tags=["Prepared Workouts"])


@router.get("/{workout_id}", response_model=PreparedWorkoutOut)
async def get_workout_by_id(
    workout_id: int,
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    workout = await get_prepared_workout_by_id(workout_id=workout_id, session=db)
    return workout