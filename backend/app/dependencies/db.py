"""Database dependency injection provider."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Dependency that provides an async database session per request."""
    async for session in get_db_session():
        yield session
