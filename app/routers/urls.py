from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.db.schema import get_session
from app.models.url import URL, URLCreate
from app.utils.shortcode import generate_short_code

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/{short_code}")
def redirect_url(short_code: str, session: SessionDep) -> RedirectResponse:
    url = session.exec(select(URL).where(URL.short_code == short_code)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url.original_url)


@router.get("/urls/")
def read_urls(session: SessionDep) -> list[URL]:
    return session.exec(select(URL)).all()


@router.get("/urls/{short_code}")
def read_url(short_code: str, session: SessionDep) -> URL:
    url = session.exec(select(URL).where(URL.short_code == short_code)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


@router.post("/urls/")
def create_url(data: URLCreate, session: SessionDep) -> URL:
    for _ in range(5):
        url = URL(original_url=data.original_url, short_code=generate_short_code())
        session.add(url)
        try:
            session.commit()
            session.refresh(url)
            return url
        except IntegrityError:
            session.rollback()
    raise HTTPException(status_code=500, detail="Could not generate unique short code")