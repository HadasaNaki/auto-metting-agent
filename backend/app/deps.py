from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://smart:agent@db:5432/smartagent")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

security = HTTPBearer()


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user():
    """Get current authenticated user from JWT token"""
    # JWT validation logic here
    pass


def get_current_org():
    """Get current organization from authenticated user"""
    # Organization extraction logic here
    pass
