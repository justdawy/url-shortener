from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.db.schema import get_session
from app.models.url import URL, URLCreate, URLUpdate, URLPublic
from app.utils.shortcode import generate_short_code

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/{short_code}")
def redirect_url(short_code: str, session: SessionDep) -> RedirectResponse:
    url: URL = session.exec(select(URL).where(URL.short_code == short_code)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    url.clicks += 1
    session.add(url)
    session.commit()
    return RedirectResponse(url=url.original_url)


@router.get("/urls/", response_model=list[URLPublic])
def read_urls(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return session.exec(select(URL).offset(offset).limit(limit)).all()


@router.get("/urls/{short_code}", response_model=URLPublic)
def read_url(short_code: str, session: SessionDep):
    url = session.exec(select(URL).where(URL.short_code == short_code)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


@router.post("/urls/", response_model=URLPublic)
def create_url(data: URLCreate, session: SessionDep):
    for _ in range(5):
        url = URL(original_url=str(data.original_url), short_code=generate_short_code())
        session.add(url)
        try:
            session.commit()
            session.refresh(url)
            return url
        except IntegrityError:
            session.rollback()
    raise HTTPException(status_code=500, detail="Could not generate unique short code")

@router.patch("/urls/", response_model=URLPublic)
def update_url(short_code: str, data: URLUpdate, session: SessionDep):
    url = session.exec(select(URL).where(URL.short_code == short_code)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if data.original_url is not None:
        url.original_url = str(data.original_url)
    if data.short_code is not None:
        url.short_code = data.short_code

    session.add(url)
    try:
        session.commit()
        session.refresh(url)
        return url
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="short_code already exists")

@router.delete("/urls/{short_code}")
def delete_url(short_code: str, session: SessionDep):
    url = session.exec(select(URL).where(URL.short_code == short_code)).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    session.delete(url)
    session.commit()
    return {"ok": True}