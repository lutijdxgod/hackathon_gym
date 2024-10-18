from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import MuscleGroup


async def get_muscle_groups(session: AsyncSession):
    query = select(MuscleGroup)
    query_result = await session.execute(query)
    result = query_result.all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result
