"""
Scheduling2.0 - Database Configuration
Merged database setup combining features from both projects
"""

import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://scheduling_user:scheduling_pass123@localhost:5432/scheduling2_db"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create sync engine and session factory for tools that need sync access
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Convert async URL to sync URL
sync_database_url = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')

sync_engine = create_engine(
    sync_database_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

# Create declarative base
Base = declarative_base()

# Dependency to get database session
async def get_db() -> AsyncSession:
    """
    Dependency function to get database session.
    Yields an async database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Create all tables
async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Drop all tables (for testing)
async def drop_tables():
    """Drop all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 