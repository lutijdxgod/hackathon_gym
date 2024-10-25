from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import db_helper as db
from app.models.models import Equipment
from app.oauth2 import get_current_user
from app.schemas.equipment import EquipmentInfo
from app.api.functions.funcs import (
    get_single_entity_by_field,
)
from app.schemas.users import UserOut

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.get("/{id}", response_model=EquipmentInfo)
async def get_equipment_by_id(
    id: int = Path(...), db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    equipment = await get_single_entity_by_field(entity=Equipment, field=Equipment.id, value=id, session=db)
    return equipment
