from pydantic import BaseModel

from app.schemas.exercises import ExerciseInWorkout


class PreparedWorkoutOut(BaseModel):
    name: str
    description: str
    exercises: list[ExerciseInWorkout]
