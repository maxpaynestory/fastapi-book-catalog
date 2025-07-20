import pytest
from sqlalchemy import text
from app.models.database import engine, AsyncSessionLocal
from app.models.book import BookCreate, BookUpdate, Base
from app.models.crud_book import create_book, get_books, update_book, delete_book
import asyncio

@pytest.fixture(autouse=True)
def clear_books():
    async def setup_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with AsyncSessionLocal() as db:
            await db.execute(text("DELETE FROM books"))
            await db.commit()
    asyncio.run(setup_db())

@pytest.fixture
def db_session():
    
    class SessionWrapper:
        def __init__(self):
            self.session = None
        def __enter__(self):
            async def get_session():
                async with AsyncSessionLocal() as session:
                    self.session = session
            asyncio.run(get_session())
            return self.session
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.session:
                asyncio.run(self.session.close())
    with SessionWrapper() as session:
        yield session

def test_create_book(db_session):
    book = BookCreate(title="UnitTest", author="Tester", published_year=2022, summary="Unit test book")
    db_book = create_book(db_session, book)
    assert db_book.title == "UnitTest"
    assert db_book.author == "Tester"
    assert db_book.published_year == 2022
    assert db_book.summary == "Unit test book"

def test_get_books(db_session):
    book1 = BookCreate(title="Book1", author="A", published_year=2020)
    book2 = BookCreate(title="Book2", author="B", published_year=2021)
    create_book(db_session, book1)
    create_book(db_session, book2)
    books = get_books(db_session)
    titles = [b.title for b in books]
    assert "Book1" in titles and "Book2" in titles

def test_update_book(db_session):
    book = BookCreate(title="OldTitle", author="Author", published_year=2020)
    db_book = create_book(db_session, book)
    update = BookUpdate(title="NewTitle")
    updated = update_book(db_session, db_book.id, update)
    assert updated.title == "NewTitle"

def test_delete_book(db_session):
    book = BookCreate(title="DeleteMe", author="Author", published_year=2021)
    db_book = create_book(db_session, book)
    deleted = delete_book(db_session, db_book.id)
    assert deleted.id == db_book.id
    books = get_books(db_session)
    assert all(b.id != db_book.id for b in books)
