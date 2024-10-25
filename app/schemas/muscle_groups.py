from pydantic import BaseModel


class MuscleGroupOut(BaseModel):
    id: int
    name: str
    image_url: str
