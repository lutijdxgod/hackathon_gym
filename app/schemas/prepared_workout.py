from pydantic import BaseModel

from app.models.models import TrainingLevel
from app.schemas.exercises import ExerciseInWorkout


class PreparedWorkoutOut(BaseModel):
    name: str
    description: str
    training_level: TrainingLevel
    exercises: list[ExerciseInWorkout]
