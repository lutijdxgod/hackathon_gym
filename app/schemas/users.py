from pydantic import BaseModel, Field


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


class UserLogin(BaseModel):
    phone_number: str
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    surname: str


class SubscriptionOut(BaseModel):
    id: str
    price: int
