"""
Analysis model for storing agent analysis results.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.core.database import Base


class Analysis(Base):
    """Analysis database model."""
    
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Analysis type and status
    analysis_type = Column(String(100), nullable=False)  # price_estimation, location_analysis, deal_evaluation
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    
    # Agent results
    price_estimator_result = Column(JSON, nullable=True)
    location_analyzer_result = Column(JSON, nullable=True)
    deal_evaluator_result = Column(JSON, nullable=True)
    
    # Combined analysis
    combined_score = Column(Float, nullable=True)
    confidence_level = Column(Float, nullable=True)
    recommendations = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    property = relationship("Property", backref="analyses")
    user = relationship("User", backref="analyses")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, type='{self.analysis_type}', status='{self.status}')>"


# Pydantic models for API
class AnalysisBase(BaseModel):
    """Base analysis model."""
    property_id: int
    analysis_type: str
    status: str = "pending"


class AnalysisCreate(AnalysisBase):
    """Analysis creation model."""
    pass


class AnalysisUpdate(BaseModel):
    """Analysis update model."""
    status: Optional[str] = None
    price_estimator_result: Optional[Dict[str, Any]] = None
    location_analyzer_result: Optional[Dict[str, Any]] = None
    deal_evaluator_result: Optional[Dict[str, Any]] = None
    combined_score: Optional[float] = None
    confidence_level: Optional[float] = None
    recommendations: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None


class AnalysisInDB(AnalysisBase):
    """Analysis in database model."""
    id: int
    user_id: int
    price_estimator_result: Optional[Dict[str, Any]] = None
    location_analyzer_result: Optional[Dict[str, Any]] = None
    deal_evaluator_result: Optional[Dict[str, Any]] = None
    combined_score: Optional[float] = None
    confidence_level: Optional[float] = None
    recommendations: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AnalysisResponse(AnalysisBase):
    """Analysis response model."""
    id: int
    user_id: int
    price_estimator_result: Optional[Dict[str, Any]] = None
    location_analyzer_result: Optional[Dict[str, Any]] = None
    deal_evaluator_result: Optional[Dict[str, Any]] = None
    combined_score: Optional[float] = None
    confidence_level: Optional[float] = None
    recommendations: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
