import random
import string
from typing import Optional
from sqlalchemy.orm import Session
from db.models import URL
from models.model_url import URLCreate

def generate_short_url(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def shorten_url(db: Session, url_data: URLCreate) -> URL:
    short_url = generate_short_url()
    while db.query(URL).filter(URL.short_url == short_url).first() is not None:
        short_url = generate_short_url()
    
    new_url = URL(long_url=url_data.long_url, short_url=short_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def get_url(db: Session, short_url: str) -> Optional[str]:
    try:
        get_url_query = db.query(URL).filter(URL.short_url == short_url).first()
        if get_url_query:
            return get_url_query.long_url
        return None
    except Exception as e:
        print(f"An error occurred while retrieving the URL: {str(e)}")
        return None
