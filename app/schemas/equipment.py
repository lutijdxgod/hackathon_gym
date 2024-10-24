from pydantic import BaseModel


class EquipmentInfo(BaseModel):
    id: int
    name: str
    image_url: str
