from pydantic import BaseModel, model_validator

from app.models.models import TrainingLevel
from app.schemas.exercises import ExerciseInWorkout
from app.schemas.muscle_groups import MuscleGroupOut


class PreparedWorkoutOut(BaseModel):
    name: str
    description: str
    training_level: TrainingLevel
    exercises: list[ExerciseInWorkout]


class MuscleGroupIds(BaseModel):
    ids: list[int]


class PreparedWorkoutByMuscleGroups(BaseModel):
    id: int
    name: str
    description: str
    training_level: TrainingLevel
    muscle_groups: list[MuscleGroupOut]

    # @model_validator(mode="after")
    # def aggregate_exercises_by_muscle_group(self, values: dict):
    #     exercises = values.pop("exercises")

    #     muscle_group_list = []

    #     for exercise in exercises:
    #         muscle_group = exercise["exercise"]["muscle_group"]
    #         muscle_group_list.append(muscle_group)

    #     muscle_groups = list(set(muscle_group_list))
    #     values["muscle_groups"] = muscle_groups
    #     return values
