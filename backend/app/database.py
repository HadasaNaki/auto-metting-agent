"""
Database configuration and utilities
הגדרות מסד נתונים וכלי עזר
"""

import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://smart:agent123@localhost:5432/smartagent"
)

# Convert to async URL if needed
if DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Create async engine
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def get_async_session():
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """Create all tables"""
    print("🗄️ Creating database tables...")
    try:
        # Import models to register them
        from app.models import (
            Organization,
            User,
            Customer,
            Call,
            Transcript,
            Extraction,
            Job,
            Appointment,
            Message,
            Integration,
        )

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Database tables created successfully")
        return True

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


def test_connection():
    """Test database connection"""
    try:
        # Create sync engine for testing
        sync_engine = create_engine(DATABASE_URL)
        with sync_engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection
    test_connection()

    # Create tables
    asyncio.run(create_tables())
