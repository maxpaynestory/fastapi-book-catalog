


from fastapi import FastAPI
from app.routers import book
from app.models.database import engine, Base
import asyncio
from contextlib import asynccontextmanager

"""
Main entry point for the FastAPI Book Catalog application.

This module initializes the FastAPI app, sets up the async database tables using the lifespan event,
and includes the book router for all book-related API endpoints.
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler.
    Creates all database tables asynchronously at application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint for health check or welcome message.
    Returns a simple JSON greeting.
    """
    return {"message": "Hello, World!"}

# Include the book router for all /books endpoints
app.include_router(book.router)
