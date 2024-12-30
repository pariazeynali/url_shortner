from pydantic import BaseModel, HttpUrl

class URLCreate(BaseModel):
    long_url: str

class URLResponse(BaseModel):
    long_url: str
    short_url: str
