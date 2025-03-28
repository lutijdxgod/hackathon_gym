from datetime import datetime
from typing import Annotated, Any
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Enum,
    ForeignKey,
)
from enum import Enum as ENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

str_not_nullable_an = Annotated[str, mapped_column(nullable=False)]
str_nullable_an = Annotated[str | None, mapped_column(nullable=True)]
float_not_nullable_an = Annotated[float, mapped_column(nullable=False)]
float_nullable_an = Annotated[float | None, mapped_column(nullable=True)]
int_not_nullable_an = Annotated[int, mapped_column(nullable=False)]
int_nullable_an = Annotated[int | None, mapped_column(nullable=True)]
phone_number_an = Annotated[str, mapped_column(String(10), nullable=False)]
datetime_now_not_nullable_an = Annotated[
    datetime,
    mapped_column(TIMESTAMP, nullable=False, server_default=func.now()),
]


class Sex(str, ENUM):
    male = "Male"
    female = "Female"


class TrainingLevel(str, ENUM):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class TrainingFrequency(str, ENUM):
    low = "low"
    medium = "medium"
    high = "high"


class MediaType(str, ENUM):
    image = "image"
    video = "video"


class TrainingPurpose(str, ENUM):
    gaining_weight = "Набор веса"
    gaining_muscle_weight = "Набор мышечной массы"
    losing_fat = "Похудение"
    maintaining = "Поддержание формы"


class AdviceType(str, ENUM):
    training_plan = "План тренировки"
    progress = "Прогресс"


class User(Base):
    __tablename__ = "users"

    name: Mapped[str_not_nullable_an]
    surname: Mapped[str_not_nullable_an]
    phone_number: Mapped[phone_number_an]
    password: Mapped[str_not_nullable_an]
    created_at: Mapped[datetime_now_not_nullable_an]

    user_info: Mapped["UserInfo"] = relationship(back_populates="user")


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sex: Mapped[Sex] = mapped_column(nullable=False)
    image_url: Mapped[str_nullable_an]
    date_of_birthday: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    weight: Mapped[float_not_nullable_an]
    height: Mapped[int_not_nullable_an]
    training_level: Mapped[TrainingLevel] = mapped_column(nullable=False)
    training_frequency: Mapped[TrainingFrequency] = mapped_column(nullable=False)
    training_purpose: Mapped[TrainingPurpose] = mapped_column(nullable=False)
    todays_muscle_group_id: Mapped[int] = mapped_column(ForeignKey("muscle_groups.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="user_info")


class UserVerification(Base):
    __tablename__ = "user_verification"

    user_id: Mapped[int] = mapped_column(unique=True, nullable=True)
    phone_number: Mapped[phone_number_an]
    verification_code: Mapped[str] = mapped_column(String(length=4), nullable=True)


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    gym_id: Mapped[int] = mapped_column(ForeignKey("gyms.id"), nullable=False)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    price: Mapped[int] = mapped_column()
    notify: Mapped[bool] = mapped_column(server_default="False")

    gym: Mapped["Gym"] = relationship(primaryjoin="Subscription.gym_id == Gym.id")


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    name: Mapped[str_not_nullable_an]
    image_url: Mapped[str_not_nullable_an]


class Equipment(Base):
    __tablename__ = "equipment"

    name: Mapped[str_not_nullable_an]
    image_url: Mapped[str_not_nullable_an]

    exercises: Mapped[list["Exercise"]] = relationship(back_populates="equipment")
    gym_equipments: Mapped["GymEquipments"] = relationship(back_populates="equipment")


class Exercise(Base):
    __tablename__ = "exercises"

    name: Mapped[str_not_nullable_an]
    description: Mapped[str_not_nullable_an]
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), nullable=False)
    muscle_group_id: Mapped[int] = mapped_column(ForeignKey("muscle_groups.id"), nullable=False)
    image_url: Mapped[str_not_nullable_an]
    difficulty: Mapped[TrainingLevel] = mapped_column(nullable=False)

    equipment: Mapped["Equipment"] = relationship(
        back_populates="exercises",
        primaryjoin="Exercise.equipment_id == Equipment.id",
    )
    exercise_media: Mapped[list["ExerciseMedia"]] = relationship(
        back_populates="exercises",
        primaryjoin="Exercise.id == ExerciseMedia.exercise_id",
    )
    muscle_group: Mapped[list["MuscleGroup"]] = relationship(primaryjoin="MuscleGroup.id == Exercise.muscle_group_id")


class ExerciseMedia(Base):
    __tablename__ = "exercise_media"

    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    type: Mapped[MediaType] = mapped_column(nullable=False)
    url: Mapped[str_not_nullable_an]

    exercises: Mapped["Exercise"] = relationship(back_populates="exercise_media")


class Gym(Base):
    __tablename__ = "gyms"

    name: Mapped[str_not_nullable_an]
    image_url: Mapped[str_not_nullable_an]


class AIAdvice(Base):
    __tablename__ = "ai_advice"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[AdviceType] = mapped_column(nullable=False)
    message: Mapped[str_not_nullable_an]
    created_at: Mapped[datetime_now_not_nullable_an]


class PreparedWorkout(Base):
    __tablename__ = "prepared_workouts"

    name: Mapped[str_not_nullable_an]
    description: Mapped[str_not_nullable_an]
    training_level: Mapped[TrainingLevel] = mapped_column(nullable=False)

    exercises: Mapped[list["PreparedWorkoutsExercises"]] = relationship(
        primaryjoin="PreparedWorkoutsExercises.workout_id == PreparedWorkout.id",
        join_depth=3,
    )


class PreparedWorkoutsExercises(Base):
    __tablename__ = "prepared_workouts_exercises"

    workout_id: Mapped[int] = mapped_column(ForeignKey("prepared_workouts.id"), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False)
    sets: Mapped[int_not_nullable_an]
    repetitions: Mapped[int_not_nullable_an]
    weight: Mapped[int_nullable_an]

    exercise: Mapped["Exercise"] = relationship(primaryjoin="Exercise.id == PreparedWorkoutsExercises.exercise_id")


class FavoriteWorkout(Base):
    __tablename__ = "favorite_workouts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    workout_id: Mapped[int] = mapped_column(ForeignKey("prepared_workouts.id"))


class GymEquipments(Base):
    __tablename__ = "gym_equipments"

    gym_id: Mapped[int_not_nullable_an] = mapped_column(ForeignKey("gyms.id"))
    equipment_id: Mapped[int_not_nullable_an] = mapped_column(ForeignKey("equipment.id"))

    equipment: Mapped["Equipment"] = relationship(back_populates="gym_equipments")


class MyTraining(Base):
    __tablename__ = "my_training"
    name: Mapped[str_not_nullable_an]
    training_frequency: Mapped[TrainingFrequency] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    my_training_exercises: Mapped[list["MyTrainingExercises"]] = relationship(
        back_populates="my_training", cascade="all, delete-orphan", passive_deletes=True
    )


class MyTrainingExercises(Base):
    __tablename__ = "my_training_exercises"
    training_id: Mapped[int_not_nullable_an] = mapped_column(ForeignKey("my_training.id", ondelete="cascade"))
    sets: Mapped[int_not_nullable_an]
    repetitions: Mapped[int_not_nullable_an]
    exercise_name: Mapped[str_not_nullable_an]
    my_training: Mapped["MyTraining"] = relationship(back_populates="my_training_exercises")
