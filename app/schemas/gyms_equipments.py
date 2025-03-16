from pydantic import BaseModel

from app.schemas.equipment import EquipmentInfo

    
class GymEquipmentsById(BaseModel):
    equipment_id: int
    gym_id: int     
    equipment: EquipmentInfo