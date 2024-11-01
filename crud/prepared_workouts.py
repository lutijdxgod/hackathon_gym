from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import PreparedWorkout, PreparedWorkoutsExercises


async def get_prepared_workout_by_id(workout_id: int, session: AsyncSession):
    workout_query = (
        select(PreparedWorkout)
        .where(PreparedWorkout.id == workout_id)
        .options(selectinload(PreparedWorkout.exercises).joinedload(PreparedWorkoutsExercises.exercise))
    )
    query_result = await session.scalars(workout_query)
    workout = query_result.first()
    return workout
