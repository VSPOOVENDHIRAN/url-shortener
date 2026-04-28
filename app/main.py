from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
import re

from .db import SessionLocal, engine, Base
from . import models
from .schemas import URLCreate
from .utils import encode_base62, check_rate_limit, normalize_url
from .redis_client import redis_client

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# create tables
Base.metadata.create_all(bind=engine)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HOME PAGE (ONLY ONE)
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )

#  SHORTEN API
@app.post("/shorten")
def shorten_url(
    request: URLCreate,
    db: Session = Depends(get_db),
    req: Request = None
):
    check_rate_limit(req)

    BASE_URL = str(req.base_url).rstrip("/")

    #  EXPIRY LOGIC
    expiry_time = None
    if request.expiry_minutes:
        expiry_time = datetime.utcnow() + timedelta(minutes=request.expiry_minutes)
    clean_url = normalize_url(request.url)
    
        #  CUSTOM ALIAS
    if request.custom_code:
        if not re.match("^[a-zA-Z0-9_-]{3,15}$", request.custom_code):
            raise HTTPException(400, "Invalid custom alias")

        existing = db.query(models.URL).filter(
            models.URL.short_code == request.custom_code
        ).first()

        if existing:
            raise HTTPException(400, "Custom alias already taken")

        
        new_url = models.URL(
        original_url=clean_url,
        short_code=request.custom_code,
        expiry=expiry_time
        )
        

        db.add(new_url)
        db.commit()

        return {"short_url": f"{BASE_URL}/{request.custom_code}"}

    #  REUSE LOGIC\
   

    existing = db.query(models.URL).filter(
        models.URL.original_url == clean_url
    ).first()
  

    if existing:
        if existing.expiry is None or existing.expiry > datetime.utcnow():
            return {"short_url": f"{BASE_URL}/{existing.short_code}"}

    #  CREATE NEW
    new_url = models.URL(original_url=clean_url, short_code="", expiry=expiry_time)
    db.add(new_url)
    db.flush()

    short_code = encode_base62(new_url.id)
    new_url.short_code = short_code

    db.commit()

    return {"short_url": f"{BASE_URL}/{short_code}"}

#  REDIRECT
@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

    #  REDIS CHECK
    cached_url = None

    try:
        if redis_client:
            cached_url = redis_client.get(short_code)
            if cached_url:
                cached_url = cached_url.decode("utf-8")
    except:
        print(" Redis not available")

    if cached_url:
        print(" REDIS HIT")

        url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        if url:
            #  EXPIRY CHECK
            if url.expiry and url.expiry < datetime.utcnow():
                raise HTTPException(410, "Link expired")

            url.click_count += 1
            db.commit()

        return RedirectResponse(cached_url, status_code=302)

    print(" DB HIT")

    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if not url:
        raise HTTPException(404, "URL not found")

    # EXPIRY CHECK
    if url.expiry and url.expiry < datetime.utcnow():
        raise HTTPException(410, "Link expired")

    #  CACHE (with TTL)
    try:
        if redis_client:
            redis_client.set(short_code, url.original_url, ex=3600)
    except:
        pass

    url.click_count += 1
    db.commit()

    return RedirectResponse(url.original_url, status_code=302)


from datetime import datetime

@app.get("/stats/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if not url:
       raise HTTPException(status_code=404, detail="URL not found")
    
    print(f"Stats requested for short code: {short_code}, Original URL: {url.original_url}, Clicks: {url.click_count}, Expiry: {url.expiry}, Created At: {url.created_at}")

    return {
        "original_url": url.original_url,
        "clicks": url.click_count,
        "expiry": url.expiry,
        "created_at": url.created_at,
        "is_expired": url.expiry < datetime.utcnow() if url.expiry else False
    }