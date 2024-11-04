from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.functions.funcs import (
    extract_muscle_groups_from_prepared_workout,
    sqlalchemy_model_to_dict,
    sqlalchemy_model_to_dict_for_join,
)
from app.models.models import (
    Exercise,
    MuscleGroup,
    PreparedWorkout,
    PreparedWorkoutsExercises,
)


async def get_prepared_workout_by_id(workout_id: int, session: AsyncSession):
    workout_query = (
        select(PreparedWorkout)
        .where(PreparedWorkout.id == workout_id)
        .options(
            selectinload(PreparedWorkout.exercises).joinedload(
                PreparedWorkoutsExercises.exercise
            )
        )
    )
    query_result = await session.scalars(workout_query)
    workout = query_result.first()
    return workout


async def get_prepared_workout_by_muscle_group_ids(
    muscle_group_ids: list[int], session: AsyncSession
):
    workouts_query = (
        select(PreparedWorkout)
        .distinct()
        .options(
            selectinload(PreparedWorkout.exercises)
            .selectinload(PreparedWorkoutsExercises.exercise)
            .selectinload(Exercise.muscle_group)
        )
    )
    query_result = await session.scalars(workouts_query)
    workouts = query_result.all()

    workouts_to_return = []
    for workout in workouts:
        workout = sqlalchemy_model_to_dict_for_join(row=workout)
        print(workout)
        workout_to_check = extract_muscle_groups_from_prepared_workout(workout)
        workout_ids = [
            muscle_group["id"]
            for muscle_group in workout_to_check["muscle_groups"]
        ]
        if set(muscle_group_ids).issubset(set(workout_ids)):
            workouts_to_return.append(workout_to_check)
    return workouts_to_return
