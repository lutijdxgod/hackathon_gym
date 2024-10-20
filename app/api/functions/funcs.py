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


async def get_entity_by_field_nullable(
    entity: Table,
    field: InstrumentedAttribute,
    value: Any,
    session: AsyncSession,
):
    query = select(entity).where(field == value)
    query_result = await session.scalars(query)
    result = query_result.all()

    return result


def db_row_ids_to_str(element):
    # TODO replace __dict__ because it contains unnecessary entries
    element_dict: dict[str, Any] = element.__dict__
    for attr, val in element_dict.items():
        if attr.endswith("_id") or attr == "id":
            element_dict[attr] = str(val)
    return element_dict


def ids_to_string(elements):
    if isinstance(elements, list):
        processed_elements = []
        for i in range(len(elements)):
            processed_elements.append(db_row_ids_to_str(element=elements[i]))
        return processed_elements
    else:
        return db_row_ids_to_str(element=elements)
