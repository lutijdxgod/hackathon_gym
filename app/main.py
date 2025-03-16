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
from .api.equipment.router import router as equipment_router
from .api.ai_advice.router import router as ai_router
from .api.prepared_workouts.router import router as prepared_workouts_router
from .api.gyms_equipment.router import router as gyms_equipment_router
from .api.my_training.router import router as my_training_router


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

routers = [
    muscle_groups_router,
    exercises_router,
    auth_router,
    user_router,
    equipment_router,
    ai_router,
    prepared_workouts_router,
    gyms_equipment_router,
    my_training_router,
]
for router in routers:
    app.include_router(router)


@app.get("/ping")
async def root():
    return {"success": True, "message": " pong"}
