from pydantic import BaseModel

from app.models.models import TrainingLevel
from app.schemas.equipment import EquipmentInfo
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
