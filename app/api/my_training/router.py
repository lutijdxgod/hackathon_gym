from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import MyTraining, MyTrainingExercises
from app.oauth2 import get_current_user
from app.schemas.my_training import AddExercisesToTraining, GettingMyTraining, MyTrainingCreate
from app.schemas.users import UserOut
from app.models.database import db_helper as db

router = APIRouter(prefix="/my_training", tags=["My Training"])


@router.get("/{id}", response_model=GettingMyTraining)
async def get_my_training(
    id: int = Path(...), db: AsyncSession = Depends(db.session_getter), user: UserOut = Depends(get_current_user)
):
    get_training_query = (
        select(MyTraining)
        .filter(MyTraining.id == id, MyTraining.user_id == user.id)
        .options(selectinload(MyTraining.my_training_exercises))
    )
    result = await db.execute(get_training_query)
    my_training = result.scalar_one_or_none()
    if not my_training:
        raise HTTPException(status_code=404, detail="Training not found")

    return my_training


@router.post("/create_my_training")
async def create_my_training(
    training_data: MyTrainingCreate,
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    checking_name_training_query = select(MyTraining).filter(
        MyTraining.name == training_data.name, MyTraining.user_id == user.id
    )
    result = await db.execute(checking_name_training_query)
    getting_names = result.scalar_one_or_none()

    if getting_names:
        raise HTTPException(status_code=400, detail=f"Training with name {training_data.name} already exists.")

    new_training = MyTraining(
        name=training_data.name, training_frequency=training_data.training_frequency, user_id=user.id
    )

    db.add(new_training)
    await db.flush()

    training_exercises = [
        MyTrainingExercises(
            training_id=new_training.id, sets=ex.sets, repetitions=ex.repetitions, exercise_name=ex.name
        )
        for ex in training_data.exercises
    ]

    db.add_all(training_exercises)
    await db.commit()
    await db.refresh(new_training)

    return {"detail": "success"}


@router.put("/add_exercises/{my_training_id}")
async def add_exercises(
    training_exercises: AddExercisesToTraining,
    my_training_id: int = Path(..., description="Training ID in which to add exercises."),
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    update_training = select(MyTraining).filter(MyTraining.id == my_training_id, MyTraining.user_id == user.id)
    result = await db.execute(update_training)
    getting_training_id = result.scalar_one_or_none()

    if not getting_training_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Training not found")

    new_exercise = [
        MyTrainingExercises(training_id=my_training_id, sets=ex.sets, repetitions=ex.repetitions, exercise_name=ex.name)
        for ex in training_exercises.exercises
    ]
    db.add_all(new_exercise)
    await db.commit()

    return {"detail": "exercises were added successfully!"}


@router.delete("/{my_training_id}")
async def delete_my_training(
    my_training_id: int = Path(..., description="ID training which need delete"),
    db: AsyncSession = Depends(db.session_getter),
    user: UserOut = Depends(get_current_user),
):
    delete_training_query = select(MyTraining).filter(MyTraining.id == my_training_id, MyTraining.user_id == user.id)
    result = await db.execute(delete_training_query)
    training = result.scalar_one_or_none()

    if not training:
        raise HTTPException(status_code=404, detail=f"Not found training with {my_training_id} id")
    await db.delete(training)
    await db.commit()

    return {"detail": "successfully!"}
