from fastapi import APIRouter, Depends, Path
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.functions.funcs import get_entity_by_field
from app.models.database import db_helper as db
from app.models.models import Exercise
from app.oauth2 import get_current_user
from app.schemas.users import UserOut
from app.integrations.yandexgptmanager import (
    send_request,
    advice_for_exercise,
    advice_for_exercise_format,
    advice_for_training_plan,
    advice_for_training_plan_format,
    progress_assessment,
    progress_assessment_format,
)

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/exercise/{id}")
async def get_advice_for_exercise(
    id: int = Path(...), db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    exercise_query = select(Exercise).where(Exercise.id == id).options(joinedload(Exercise.equipment))
    query_result = await db.scalars(exercise_query)

    exercise = query_result.first()
    advice = send_request(
        message=advice_for_exercise.format(
            sex=user.user_info.sex,
            weight=user.user_info.weight,
            height=user.user_info.height,
            training_level=user.user_info.training_level,
            training_frequency=user.user_info.training_frequency,
            exercise_name=exercise.name,
            equipment_name=exercise.equipment.name,
        ),
        msg_format=advice_for_exercise_format,
    )

    return {"message": advice}


@router.get("/training_plan")
async def get_advice_for_training_plan(
    db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    # training_plan_query = select()
    advice = send_request(
        message=advice_for_training_plan.format(
            sex=user.user_info.sex,
            weight=user.user_info.weight,
            height=user.user_info.height,
            training_level=user.user_info.training_level,
            training_frequency=user.user_info.training_frequency,
        ),
        msg_format=advice_for_training_plan_format,
    )
    return {"message": advice}


@router.get("/progress_assessment")
async def get_progress_assessment(
    db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    # training_plan_query = select()
    advice = send_request(
        message=progress_assessment.format(
            sex=user.user_info.sex,
            weight=user.user_info.weight,
            height=user.user_info.height,
            training_level=user.user_info.training_level,
            training_frequency=user.user_info.training_frequency,
        ),
        msg_format=progress_assessment_format,
    )
    return {"message": advice}
