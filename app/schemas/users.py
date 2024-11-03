from datetime import datetime
import json
from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator, validator

from app.models.models import Sex, TrainingFrequency, TrainingLevel, TrainingPurpose


class UserCreate(BaseModel):
    phone_number: str


class Token(BaseModel):
    access_token: str = Field(
        name="Access Token",
        description="Токен",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MjI0NTkyNzV9.14pWxb2M9Ig3yYXrLndyhd7UzwHI4hcKbgYomjYUhAQ"
        ],
    )
    token_type: str = Field(name="Token Type", description="Тип токена", examples=["Bearer"])
    user_id: str = Field(name="User ID", description="User ID Field", examples=["15"])


class TokenData(BaseModel):
    user_id: str | None


class UserInfo(BaseModel):
    sex: Sex
    date_of_birthday: datetime = Field(name="Date Of Birthday", examples=["2004-08-31T00:00:00.000"])
    image_url: str
    weight: float
    height: int
    training_level: TrainingLevel
    training_frequency: TrainingFrequency
    training_purpose: TrainingPurpose


class UserRegisterCheckCode(BaseModel):
    phone_number: str
    verification_code: str
    password: str
    name: str = Field(name="Name", description="String that represents User's name", examples=["Тоха"])
    surname: str = Field(
        name="Surname",
        description="String that represents User's surname",
        examples=["Мыськин"],
    )
    user_info: UserInfo


class UserLogin(BaseModel):
    phone_number: str
    password: str


class SubscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    price: int
    end_time: datetime
    gym_name: str = Field(validation_alias=AliasPath("gym", "name"))
    gym_avatar: str | None = Field(validation_alias=AliasPath("gym", "image_url"))
    is_notificated: bool = Field(..., alias="notify")


class UserOut(BaseModel):
    id: int
    name: str
    surname: str
    user_info: UserInfo


class ProfileUser(BaseModel):
    phone_number: str
    name: str
    surname: str
    created_at: datetime
    user_info: UserInfo
