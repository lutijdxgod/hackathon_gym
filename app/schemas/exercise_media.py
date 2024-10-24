from pydantic import BaseModel

from app.models.models import MediaType


class ExerciseMedia(BaseModel):
    id: int
    type: MediaType
    url: str
    exercise_id: int
