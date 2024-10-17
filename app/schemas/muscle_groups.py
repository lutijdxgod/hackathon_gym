from pydantic import BaseModel


class MuscleGroupOut(BaseModel):
    name: str
    image_url: str
