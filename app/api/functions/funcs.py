from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.models.database import db_helper as db


async def get_entity_by_field(
    entity: Table,
    field: InstrumentedAttribute,
    value: Any,
    session: AsyncSession,
):
    query = select(entity).where(field == value)
    query_result = await session.scalars(query)
    result = query_result.all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result
