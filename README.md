# Book Catalog API - FastAPI Take-Home Test

This project implements a Book Catalog RESTful API using FastAPI, async SQLAlchemy (with aiosqlite), and Pydantic. It supports full CRUD operations for books, including an async endpoint for listing all books.

# Book Catalog API - FastAPI Take-Home Test

This project implements a Book Catalog RESTful API using FastAPI, async SQLAlchemy (with aiosqlite), and Pydantic. It supports full CRUD operations for books, including an async endpoint for listing all books. All endpoints are covered by integration tests.


# FastAPI Book Catalog API

This project is a modern FastAPI application implementing a Book Catalog RESTful API. It uses async SQLAlchemy with aiosqlite for database operations and follows best practices for FastAPI, Pydantic, and Python project structure.

## Getting Started


### Using pip
1. Create and activate a virtual environment (recommended):
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   # For async SQLAlchemy, aiosqlite is required
   ```
3. Run the app:
   ```sh
   uvicorn app.main:app --reload
   ```
4. Run tests (including async endpoint):
   ```sh
   python -m pytest tests
   ```


### Using Poetry
1. Install dependencies:
   ```sh
   poetry install
   ```
2. Run the app:
   ```sh
   poetry run uvicorn app.main:app --reload
   ```
3. Run tests:
   ```sh
   poetry run pytest tests
   ```

## Features
- Async CRUD endpoints for books
- Async SQLAlchemy with aiosqlite
- FastAPI lifespan event for database table creation
- Pydantic models for validation
- Pytest and pytest-asyncio for testing

## Setup
1. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the server:
   ```powershell
   uvicorn app.main:app --reload
   ```

## Additional Features
- Realistic year validation for published_year (1450 to current year)
- All request/response schemas use Pydantic models

## Project Structure
## API Endpoints
- `GET /books` - List all books
- `POST /books` - Add a new book
- `GET /books/{book_id}` - Get a book by ID
- `PUT /books/{book_id}` - Update a book
- `DELETE /books/{book_id}` - Delete a book

## Notes
- Uses FastAPI lifespan event for async table creation (no deprecated startup event)
- Only Book model is present; all user-related code removed
- `app/main.py`: Main FastAPI application
- `app/routers/book.py`: Book API endpoints (CRUD, async list)
- `app/models/book.py`: SQLAlchemy and Pydantic models for Book
- `app/models/database.py`: Database setup
- `app/models/crud_book.py`: Business logic for Book CRUD
- `tests/integration`: Integration tests for API endpoints
- `tests/unit`: Unit tests for business logic (CRUD functions)



## Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy (async)
- aiosqlite
- Pydantic
- pytest
- pytest-asyncio

## API Endpoints
- `GET /books/` — List all books (async)
- `GET /books/{id}` — Retrieve a book by ID
- `POST /books/` — Create a new book
- `PUT /books/{id}` — Update a book
- `DELETE /books/{id}` — Delete a book

## Documentation
- Interactive OpenAPI docs available at `/docs` when running the app
