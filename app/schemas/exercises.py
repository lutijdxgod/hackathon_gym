from pydantic import BaseModel


class ExerciseOut(BaseModel):
    name: str
    description: str
    equipment_id: int
