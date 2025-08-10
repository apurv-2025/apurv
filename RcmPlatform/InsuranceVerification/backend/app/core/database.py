# File: app/core/database.py (UPDATED to use effective_database_url)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# Use the effective database URL
database_url = settings.effective_database_url if hasattr(settings, 'effective_database_url') else settings.DATABASE_URL

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Database dependency that creates a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
