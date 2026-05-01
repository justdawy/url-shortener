from sqlmodel import Session, create_engine, SQLModel

from app.core.config import config

engine = create_engine(config.db_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session