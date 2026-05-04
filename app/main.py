import string
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.db.schema import create_db_and_tables
from app.routers import urls
from app.core.config import config
from app.core.redis import client as redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    redis.ping() # raises ConnectionError if Redis is not running
    yield

app = FastAPI(title=config.app_name, lifespan=lifespan)
app.include_router(urls.router)
