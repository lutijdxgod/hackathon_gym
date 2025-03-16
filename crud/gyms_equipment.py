from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import GymEquipments, Equipment

async def get_equipments_by_gym_id(gym_id: int, session: AsyncSession):
    equipment_query = select(GymEquipments).where(GymEquipments.gym_id == gym_id).options(selectinload(GymEquipments.equipment))
    query_result = await session.scalars(equipment_query)
    equipment = query_result.all()
    return equipment

