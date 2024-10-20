from math import ceil
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from .models.database import db_helper
from .config import settings
from fastapi_limiter import FastAPILimiter

from .api.muscle_groups.router import router as muscle_groups_router
from .api.exercises.router import router as exercises_router
from .api.auth.router import router as auth_router
from .api.users.router import router as user_router


async def custom_callback(request: Request, response: Response, pexpire: int):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Слишком много запросов. Попробуйте снова через {expire} секунд.",
        headers={"Retry-After": str(expire)},
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connection = redis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(
        redis=redis_connection,
        http_callback=custom_callback,
    )
    yield
    await FastAPILimiter.close()
    await db_helper.dispose()


app = FastAPI()

origins = ["*"]  # ["*"] for public api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(muscle_groups_router)
app.include_router(exercises_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/ping")
async def root():
    print(settings.auth.access_token_expire_minutes)
    return {"success": True, "message": " pong"}
