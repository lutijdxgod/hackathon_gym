from typing import Any
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.models.base import Base
from app.models.database import db_helper as db
from app.models.models import PreparedWorkout


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


def sqlalchemy_model_to_dict_for_join(row: Base | list) -> dict:
    print(type(row))
    if isinstance(row, Base):
        row_dictionary = row.__dict__

        keys_to_delete = [
            key for key in row_dictionary.keys() if key.startswith("_sa")
        ]  # or just "_"?
        for key in keys_to_delete:
            row_dictionary.pop(key)

        return dict(
            (
                (col, val)
                if not isinstance(val, (Base, list))
                else (col, sqlalchemy_model_to_dict_for_join(val))
            )
            for col, val in row.__dict__.items()
        )
    else:
        return [sqlalchemy_model_to_dict_for_join(elem) for elem in row]


def sqlalchemy_model_to_dict(row: Base) -> dict:
    return dict(
        (
            (col, val)
            if not isinstance(val := getattr(row, col), Base)
            else (col, sqlalchemy_model_to_dict(val))
        )
        for col in row.__table__.columns.keys()
    )


def extract_muscle_groups_from_prepared_workout(workout: PreparedWorkout):
    # workout = workout.__dict__
    # exercises = workout.pop("exercises")

    # muscle_group_list = []

    # for exercise in exercises:
    #     pw_exercise = exercise.__dict__
    #     exercise = pw_exercise["exercise"].__dict__
    #     muscle_group = exercise["muscle_group"]
    #     muscle_group_list.append(muscle_group)

    # muscle_groups = list(set(muscle_group_list))
    # workout["muscle_groups"] = muscle_groups
    # return workout

    exercises = workout.pop("exercises")

    muscle_group_list = []

    for exercise in exercises:
        muscle_group = exercise["exercise"]["muscle_group"]
        if not muscle_group in muscle_group_list:
            muscle_group_list.append(muscle_group)

    muscle_groups = list(muscle_group_list)
    workout["muscle_groups"] = muscle_groups
    return workout
