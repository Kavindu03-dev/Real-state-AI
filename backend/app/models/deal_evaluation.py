"""
Deal evaluation model for storing deal analysis results.
"""

from sqlalchemy import Column, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.database import Base


class DealEvaluation(Base):
    """Deal evaluation database model."""

    __tablename__ = "deal_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    deal_score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    property = relationship("Property", backref="deal_evaluations")

    def __repr__(self):
        return f"<DealEvaluation(id={self.id}, property_id={self.property_id}, deal_score={self.deal_score})>"


# Pydantic models for API
class DealEvaluationBase(BaseModel):
    """Base deal evaluation model."""
    property_id: int
    deal_score: Optional[float] = None
    confidence: Optional[float] = None
    explanation: Optional[str] = None


class DealEvaluationCreate(DealEvaluationBase):
    """Deal evaluation creation model."""
    pass


class DealEvaluationUpdate(BaseModel):
    """Deal evaluation update model."""
    deal_score: Optional[float] = None
    confidence: Optional[float] = None
    explanation: Optional[str] = None


class DealEvaluationInDB(DealEvaluationBase):
    """Deal evaluation in database model."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DealEvaluationResponse(DealEvaluationBase):
    """Deal evaluation response model."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
