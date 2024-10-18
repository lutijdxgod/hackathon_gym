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
from sqlalchemy.sql.expression import func
from .base import Base


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

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    mobile_phone = Column(String(length=10), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    image_url = Column(String, nullable=True)
    date_of_birthday = Column(TIMESTAMP, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)
    training_level = Column(Enum(TrainingLevel), nullable=False)
    training_frequency = Column(Enum(TrainingFrequency), nullable=False)


class UserVerification(Base):
    __tablename__ = "user_verification"

    user_id = Column(Integer, unique=True)
    phone_number = Column(String(length=10), nullable=False, unique=True)
    verification_code = Column(String(length=4))


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    gym_id = Column(Integer, ForeignKey("gyms.id"), nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    price = Column(Integer)


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)


class Equipment(Base):
    __tablename__ = "equipment"

    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)


class Exercise(Base):
    __tablename__ = "exercises"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    muscle_group_id = Column(
        Integer, ForeignKey("muscle_groups.id"), nullable=False
    )
    image_url = Column(String, nullable=False)


class ExerciseMedia(Base):
    __tablename__ = "exercise_media"

    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    type = Column(Enum(MediaType), nullable=False)
    url = Column(String, nullable=False)


class Gym(Base):
    __tablename__ = "gyms"

    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
