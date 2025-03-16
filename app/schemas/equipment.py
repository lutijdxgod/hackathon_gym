from pydantic import BaseModel


class EquipmentInfo(BaseModel):
    name: str
    image_url: str
