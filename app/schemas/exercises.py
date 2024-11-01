from pydantic import AliasPath, BaseModel, Field

from app.models.models import TrainingLevel
from app.schemas.exercise_media import ExerciseMedia


class ExerciseByMuscleGroup(BaseModel):
    id: int
    name: str
    description: str
    equipment_id: int
    difficulty: str


class ExerciseByMuscleGroupFiltered(BaseModel):
    id: int
    name: str
    description: str
    equipment_id: int


class ExerciseByEquipment(BaseModel):
    id: int
    name: str
    description: str
    muscle_group_id: int
    image_url: str


class ExerciseInfo(BaseModel):
    name: str
    description: str
    difficulty: TrainingLevel
    muscle_group_id: int
    image_url: str
    exercise_media: list[ExerciseMedia]


class ExerciseInList(BaseModel):
    id: int
    name: str
    description: str
    equipment_id: int
    muscle_group_id: int
    image_url: str


class ExercisesList(BaseModel):
    beginner_exercises: list[ExerciseInList]
    intermediate_exercises: list[ExerciseInList]
    advanced_exercises: list[ExerciseInList]


class ExerciseInWorkout(BaseModel):
    id: int
    name: str = Field(validation_alias=AliasPath("exercise", "name"))
    description: str = Field(validation_alias=AliasPath("exercise", "description"))
    equipment_id: int = Field(validation_alias=AliasPath("exercise", "equipment_id"))
    muscle_group_id: int = Field(validation_alias=AliasPath("exercise", "muscle_group_id"))
    image_url: str = Field(validation_alias=AliasPath("exercise", "image_url"))
    difficulty: TrainingLevel = Field(validation_alias=AliasPath("exercise", "difficulty"))
    sets: int
    repetitions: int
    weight: float | None
