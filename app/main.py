import string
import secrets

from fastapi import FastAPI
from app.db.schema import create_db_and_tables
from app.routers import urls
from app.core.config import config

app = FastAPI(title=config.app_name)
app.include_router(urls.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
