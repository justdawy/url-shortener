from datetime import datetime
from sqlmodel import Field, SQLModel

class URLCreate(SQLModel):
    original_url: str

class URL(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    clicks: int = Field(default=0)
    short_code: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)