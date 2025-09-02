"""
Location analysis model for storing location-specific data.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.database import Base


class LocationAnalysis(Base):
    """Location analysis database model."""

    __tablename__ = "location_analysis"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(500), nullable=False, index=True)
    safety_rating = Column(Float, nullable=True)
    schools = Column(Text, nullable=True)  # JSON string or text description
    transport = Column(Text, nullable=True)  # JSON string or text description
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<LocationAnalysis(id={self.id}, location='{self.location}')>"


# Pydantic models for API
class LocationAnalysisBase(BaseModel):
    """Base location analysis model."""
    location: str
    safety_rating: Optional[float] = None
    schools: Optional[str] = None
    transport: Optional[str] = None
    summary: Optional[str] = None


class LocationAnalysisCreate(LocationAnalysisBase):
    """Location analysis creation model."""
    pass


class LocationAnalysisUpdate(BaseModel):
    """Location analysis update model."""
    safety_rating: Optional[float] = None
    schools: Optional[str] = None
    transport: Optional[str] = None
    summary: Optional[str] = None


class LocationAnalysisInDB(LocationAnalysisBase):
    """Location analysis in database model."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LocationAnalysisResponse(LocationAnalysisBase):
    """Location analysis response model."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
