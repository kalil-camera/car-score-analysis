"""
Database configuration and session management
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.sqlalchemy_echo,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
