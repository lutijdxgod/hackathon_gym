from pydantic import BaseModel, Field


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
    id: str | None
