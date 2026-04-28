from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .db import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    original_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expiry = Column(TIMESTAMP, nullable=True)
    click_count = Column(Integer, default=0)