"""
Database configuration and connection management.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import redis
import asyncio

from app.core.config import settings

# Database engine
if settings.ENVIRONMENT == "test":
    # Use in-memory SQLite for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # Use PostgreSQL for production/development
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Metadata
metadata = MetaData()

# Redis connection
redis_client = None


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database."""
    global redis_client
    
    # Initialize Redis
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        print("✅ Redis connection established")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        redis_client = None
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")


def get_redis():
    """Get Redis client."""
    return redis_client


# Database models
from app.models.user import User
from app.models.property import Property
from app.models.analysis import Analysis
from app.models.agent_log import AgentLog
from app.models.location_analysis import LocationAnalysis
from app.models.deal_evaluation import DealEvaluation
