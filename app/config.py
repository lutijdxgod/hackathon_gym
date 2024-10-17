from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    hostname: str
    port: str
    password: str
    name: str
    username: str

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AWS(BaseModel):
    access_key_id: str
    secret_access_key: str
    endpoint_url: str
    bucket_name: str
    image_url_prefix: str


class Firebase(BaseModel):
    credentials: str


class Auth(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class FlashCall(BaseModel):
    public_key: str
    campaign_id: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__")

    db: Database
    aws: AWS
    firebase: Firebase
    auth: Auth
    flashcall: FlashCall


settings = Settings()
