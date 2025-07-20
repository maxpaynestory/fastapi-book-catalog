
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import AsyncSessionLocal, engine
from app.models.book import Book, BookCreate, BookUpdate, BookDB, Base
from app.models.crud_book import get_book, get_books, create_book, update_book, delete_book
from typing import List
import asyncio

router = APIRouter()




# Dependency

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["books"])
def api_create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return create_book(db, book)

@router.get("/books/{book_id}", response_model=Book, tags=["books"])
async def api_get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/books/", response_model=List[Book], tags=["books"])
def api_list_books(db: AsyncSession = Depends(get_db)):
    return get_books(db)

@router.put("/books/{book_id}", response_model=Book, tags=["books"])
def api_update_book(book_id: int, book_update: BookUpdate, db: AsyncSession = Depends(get_db)):
    updated = update_book(db, book_id, book_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
def api_delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted = delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return
