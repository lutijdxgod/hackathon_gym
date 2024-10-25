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


class Sex(str, ENUM):
    male = "Male"
    female = "Female"


class TrainingLevel(str, ENUM):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class TrainingFrequency(int, ENUM):
    low = 1
    medium = 2
    high = 3


class MediaType(str, ENUM):
    image = "image"
    video = "video"


class User(Base):
    __tablename__ = "users"

    name: Mapped[str_not_nullable_an]
    surname: Mapped[str_not_nullable_an]
    phone_number: Mapped[phone_number_an]
    password: Mapped[str_not_nullable_an]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())

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


class Exercise(Base):
    __tablename__ = "exercises"

    name: Mapped[str_not_nullable_an]
    description: Mapped[str_not_nullable_an]
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), nullable=False)
    muscle_group_id: Mapped[int] = mapped_column(ForeignKey("muscle_groups.id"), nullable=False)
    difficulty: Mapped[TrainingLevel] = mapped_column(nullable=False)

    equipment: Mapped["Equipment"] = relationship(
        back_populates="exercises", primaryjoin="Exercise.equipment_id == Equipment.id"
    )
    exercise_media: Mapped[list["ExerciseMedia"]] = relationship(
        back_populates="exercises", primaryjoin="Exercise.id == ExerciseMedia.exercise_id"
    )


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
