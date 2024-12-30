from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.session import get_db
from models.model_url import URLCreate, URLResponse
from api.services.url_service import shorten_url, get_url

router = APIRouter()

@router.post("/shorten/", response_model=URLResponse)
def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    try:
        new_url = shorten_url(db, url)
        return URLResponse(long_url=new_url.long_url, short_url=new_url.short_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{short_url}")
def redirect_url(short_url: str, db: Session = Depends(get_db)):
    try:
        long_url = get_url(db, short_url)
        if not long_url:
            raise HTTPException(status_code=404, detail="URL not found")
        return RedirectResponse(long_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
