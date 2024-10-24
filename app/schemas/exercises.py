from pydantic import BaseModel


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
