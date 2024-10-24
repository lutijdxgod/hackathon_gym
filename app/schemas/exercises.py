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


class ExerciseInfo(BaseModel):
    name: str
    description: str
    difficulty: TrainingLevel
    muscle_group_id: int
    equipment: EquipmentInfo
    exercise_media: list[ExerciseMedia]
