from sqlalchemy import text


import pytest
from app.models.database import engine, AsyncSessionLocal
from app.models.book import Base
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import AsyncSessionLocal
 





import os

@pytest.fixture(autouse=True)
def clear_books():
    """
    Synchronous fixture to ensure database and table exist before tests.
    Clears the books table before each test.
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'test.db')
    async def setup_db():
        if not os.path.exists(db_path):
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        async with AsyncSessionLocal() as db:
            try:
                await db.execute(text("DELETE FROM books"))
                await db.commit()
            except Exception:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                await db.execute(text("DELETE FROM books"))
                await db.commit()
    asyncio.run(setup_db())

client = TestClient(app)
def test_list_books():
    book1 = {"title": "Book1", "author": "A", "summary": "D1", "published_year": 2022}
    book2 = {"title": "Book2", "author": "B", "summary": "D2", "published_year": 2023}
    client.post("/books/", json=book1)
    client.post("/books/", json=book2)
    response = client.get("/books/")
    assert response.status_code == 200
    titles = [b["title"] for b in response.json()]
    assert "Book1" in titles and "Book2" in titles


def test_create_and_get_book():
    book = {"title": "Test Book", "author": "Author", "summary": "A book.", "published_year": 2025}
    response = client.post("/books/", json=book)
    assert response.status_code == 201
    book_id = response.json()["id"]
    # Only api_get_book is async, so use client.get as usual
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == book["title"]

def test_update_book():
    book = {"title": "Old Title", "author": "Author", "summary": "Desc", "published_year": 2020}
    response = client.post("/books/", json=book)
    book_id = response.json()["id"]
    update = {"title": "New Title"}
    response = client.put(f"/books/{book_id}", json=update)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_book():
    book = {"title": "Delete Me", "author": "Author", "summary": "Desc", "published_year": 2021}
    response = client.post("/books/", json=book)
    book_id = response.json()["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404


def test_list_books():
    book1 = {"title": "Book1", "author": "A", "summary": "D1", "published_year": 2022}
    book2 = {"title": "Book2", "author": "B", "summary": "D2", "published_year": 2023}
    client.post("/books/", json=book1)
    client.post("/books/", json=book2)
    response = client.get("/books/")
    assert response.status_code == 200
    titles = [b["title"] for b in response.json()]
    assert "Book1" in titles and "Book2" in titles


def test_published_year_validation():
    # Year too early
    invalid_book = {"title": "Invalid", "author": "A", "published_year": 1200}
    response = client.post("/books/", json=invalid_book)
    assert response.status_code == 422
    # Year too late
    from datetime import datetime
    future_year = datetime.now().year + 10
    invalid_book = {"title": "Invalid", "author": "A", "published_year": future_year}
    response = client.post("/books/", json=invalid_book)
    assert response.status_code == 422
    # Valid year
    valid_book = {"title": "Valid", "author": "A", "published_year": 2020}
    response = client.post("/books/", json=valid_book)
    assert response.status_code == 201
