from typing import Any
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.models.base import Base
from app.models.database import db_helper as db


async def get_single_entity_by_field(
    entity: Table,
    field: InstrumentedAttribute,
    value: Any,
    session: AsyncSession,
):
    query = select(entity).where(field == value)
    query_result = await session.scalars(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


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


async def get_entity_by_multiple_fields(
    entity: Table,
    fields: list[InstrumentedAttribute],
    session: AsyncSession,
):
    query = select(entity).where(*fields)
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


async def get_entity_by_multiple_fields_nullable(
    entity: Table,
    fields: list[InstrumentedAttribute],
    session: AsyncSession,
):
    query = select(entity).where(*fields)
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


def sqlalchemy_model_to_dict(row: Base) -> dict:
    row_dictionary = row.__dict__

    keys_to_delete = [key for key in row_dictionary.keys() if key.startswith("_sa")]  # or just "_"?
    for key in keys_to_delete:
        row_dictionary.pop(key)

    return dict(
        (col, val) if not isinstance(val, Base) else (col, sqlalchemy_model_to_dict(val))
        for col, val in row.__dict__.items()
    )
