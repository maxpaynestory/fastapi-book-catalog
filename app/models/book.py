from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import Column, Integer, String, Text
from app.models.database import Base
from datetime import datetime

class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    summary = Column(Text, nullable=True)
    published_year = Column(Integer, nullable=True)


class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: Optional[int] = None
    summary: Optional[str] = None

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    published_year: Optional[int] = Field(
        None,
        ge=1450,
        le=datetime.now().year,
        description="Year must be between 1450 and the current year."
    )
    summary: Optional[str] = None



class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    published_year: Optional[int] = Field(
        None,
        ge=1450,
        le=datetime.now().year,
        description="Year must be between 1450 and the current year."
    )
    summary: Optional[str] = None
