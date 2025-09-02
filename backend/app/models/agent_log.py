"""
Agent log model for tracking agent activities and communication.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from app.core.database import Base


class AgentLog(Base):
    """Agent log database model."""
    
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Agent information
    agent_name = Column(String(100), nullable=False)  # price_estimator, location_analyzer, deal_evaluator
    agent_type = Column(String(100), nullable=False)  # llm, nlp, data_processor
    
    # Log details
    action = Column(String(200), nullable=False)  # analyze, communicate, process_data, etc.
    status = Column(String(50), default="started")  # started, completed, failed, error
    
    # Input and output
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Performance metrics
    processing_time = Column(Float, nullable=True)  # seconds
    memory_usage = Column(Float, nullable=True)  # MB
    cpu_usage = Column(Float, nullable=True)  # percentage
    
    # Communication
    communication_type = Column(String(50), nullable=True)  # rest_api, websocket, internal
    target_agent = Column(String(100), nullable=True)
    message_id = Column(String(100), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    analysis = relationship("Analysis", backref="agent_logs")
    user = relationship("User", backref="agent_logs")
    
    def __repr__(self):
        return f"<AgentLog(id={self.id}, agent='{self.agent_name}', action='{self.action}')>"


# Pydantic models for API
class AgentLogBase(BaseModel):
    """Base agent log model."""
    agent_name: str
    agent_type: str
    action: str
    status: str = "started"


class AgentLogCreate(AgentLogBase):
    """Agent log creation model."""
    analysis_id: Optional[int] = None
    user_id: Optional[int] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    communication_type: Optional[str] = None
    target_agent: Optional[str] = None
    message_id: Optional[str] = None


class AgentLogUpdate(BaseModel):
    """Agent log update model."""
    status: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None


class AgentLogInDB(AgentLogBase):
    """Agent log in database model."""
    id: int
    analysis_id: Optional[int] = None
    user_id: Optional[int] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    communication_type: Optional[str] = None
    target_agent: Optional[str] = None
    message_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AgentLogResponse(AgentLogBase):
    """Agent log response model."""
    id: int
    analysis_id: Optional[int] = None
    user_id: Optional[int] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    communication_type: Optional[str] = None
    target_agent: Optional[str] = None
    message_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
