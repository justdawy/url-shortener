from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import AnyHttpUrl

class URLBase(SQLModel):
    original_url: str
    clicks: int = Field(default=0)
    short_code: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class URL(URLBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class URLCreate(SQLModel):
    original_url: AnyHttpUrl

class URLUpdate(SQLModel):
    original_url: AnyHttpUrl | None = None
    short_code: str | None = None

class URLPublic(URLBase):
    id: int