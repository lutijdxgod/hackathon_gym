from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.integrations.yandexgptmanager import (
    send_request,
    advice_for_training_plan,
    advice_for_training_plan_format,
    progress_assessment,
    progress_assessment_format,
)
from app.models.models import AIAdvice, AdviceType, MuscleGroup
from app.schemas.users import UserOut


async def get_advice_for_training_plan(user: UserOut, session: AsyncSession):
    # TODO: разобраться с Московским временем
    todays_date = (datetime.now(tz=timezone.utc) + timedelta(hours=3)).date()
    advice_query = select(AIAdvice).where(
        AIAdvice.user_id == user.id,
        AIAdvice.type == AdviceType.training_plan,
        func.date(AIAdvice.created_at) == todays_date,
    )
    query_result = await session.scalars(advice_query)
    advice = query_result.first()

    if advice is not None:
        return advice.message

    todays_muscle_group_id = user.user_info.todays_muscle_group_id
    if todays_muscle_group_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не выбрана группа мышц.")

    muscle_group_query = select(MuscleGroup).where(MuscleGroup.id == todays_muscle_group_id)
    query_result = await session.scalars(muscle_group_query)
    muscle_group = query_result.first()

    advice = send_request(
        message=advice_for_training_plan.format(
            muscle_group=muscle_group.name,
            sex=user.user_info.sex,
            weight=user.user_info.weight,
            height=user.user_info.height,
            training_level=user.user_info.training_level,
            training_frequency=user.user_info.training_frequency,
        ),
        msg_format=advice_for_training_plan_format,
    )
    new_advice = AIAdvice(**{"user_id": user.id, "type": AdviceType.training_plan, "message": advice})
    session.add(new_advice)
    await session.commit()

    return advice


async def assess_progress(user: UserOut, session: AsyncSession):
    # TODO: разобраться с Московским временем
    todays_date = (datetime.now(tz=timezone.utc) + timedelta(hours=3)).date()
    advice_query = select(AIAdvice).where(
        AIAdvice.user_id == user.id,
        AIAdvice.type == AdviceType.progress,
        func.date(AIAdvice.created_at) == todays_date,
    )
    query_result = await session.scalars(advice_query)
    advice = query_result.first()

    if advice is not None:
        return advice.message

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

    new_advice = AIAdvice(**{"user_id": user.id, "type": AdviceType.progress, "message": advice})
    session.add(new_advice)
    await session.commit()

    return advice
