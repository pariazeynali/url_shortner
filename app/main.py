from fastapi import FastAPI
from api.endpoints import url as url_endpoint
from db.session import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

app.include_router(url_endpoint.router, prefix="/api", tags=["URL Shortener"])
