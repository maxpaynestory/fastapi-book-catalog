
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.book import BookDB, BookCreate, BookUpdate
import asyncio

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(BookDB).filter(BookDB.id == book_id))
    return result.scalars().first()

def get_books(db: AsyncSession):
    async def inner():
        result = await db.execute(select(BookDB))
        return result.scalars().all()
    return asyncio.run(inner())

def create_book(db: AsyncSession, book: BookCreate):
    async def inner():
        db_book = BookDB(**book.model_dump())
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        return db_book
    return asyncio.run(inner())

def update_book(db: AsyncSession, book_id: int, book_update: BookUpdate):
    async def inner():
        db_book = await get_book(db, book_id)
        if not db_book:
            return None
        for field, value in book_update.model_dump(exclude_unset=True).items():
            setattr(db_book, field, value)
        await db.commit()
        await db.refresh(db_book)
        return db_book
    return asyncio.run(inner())

def delete_book(db: AsyncSession, book_id: int):
    async def inner():
        db_book = await get_book(db, book_id)
        if not db_book:
            return None
        await db.delete(db_book)
        await db.commit()
        return db_book
    return asyncio.run(inner())
