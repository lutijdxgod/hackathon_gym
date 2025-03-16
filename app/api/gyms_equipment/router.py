from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.oauth2 import get_current_user
from sqlalchemy.orm import  selectinload
from app.schemas.equipment import EquipmentInfo
from app.schemas.gyms_equipments import GymEquipmentsById
from app.schemas.users import  UserOut
from app.models.database import db_helper as db
from app.models.models import  GymEquipments
from crud.gyms_equipment import get_equipments_by_gym_id

router = APIRouter(prefix='/gyms_equipment', tags=["Gyms Equipment"])

@router.get('/{id}')
async def get_equipments_from_gym(id: int = Path(...), db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)):
    gym_equipment = await get_equipments_by_gym_id(gym_id= id, session=db)
    return [
        GymEquipmentsById(
            equipment_id=item.equipment_id,
            gym_id=item.gym_id,
            equipment=EquipmentInfo(
                name=item.equipment.name,
                image_url=item.equipment.image_url
            )
        )
        for item in gym_equipment
    ]

        
