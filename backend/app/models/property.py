"""
Property model for real estate data.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from app.core.database import Base


class Property(Base):
    """Property database model."""
    
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    zip_code = Column(String(20), nullable=False, index=True)
    property_type = Column(String(100), nullable=False)  # house, condo, townhouse, etc.
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Float, nullable=True)
    square_feet = Column(Integer, nullable=True)
    lot_size = Column(Float, nullable=True)
    year_built = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    listing_price = Column(Float, nullable=True)
    market_value = Column(Float, nullable=True)
    
    # Location data
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Property features
    features = Column(JSON, nullable=True)  # JSON object with features
    
    # Market data
    days_on_market = Column(Integer, nullable=True)
    price_per_sqft = Column(Float, nullable=True)
    property_tax = Column(Float, nullable=True)
    hoa_fees = Column(Float, nullable=True)
    
    # Status
    status = Column(String(50), default="active")  # active, sold, pending, etc.
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Property(id={self.id}, address='{self.address}')>"


# Pydantic models for API
class PropertyBase(BaseModel):
    """Base property model."""
    address: str
    city: str
    state: str
    zip_code: str
    property_type: str
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[int] = None
    lot_size: Optional[float] = None
    year_built: Optional[int] = None
    price: Optional[float] = None
    listing_price: Optional[float] = None
    market_value: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    features: Optional[Dict[str, Any]] = None
    days_on_market: Optional[int] = None
    price_per_sqft: Optional[float] = None
    property_tax: Optional[float] = None
    hoa_fees: Optional[float] = None
    status: str = "active"


class PropertyCreate(PropertyBase):
    """Property creation model."""
    pass


class PropertyUpdate(BaseModel):
    """Property update model."""
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[int] = None
    lot_size: Optional[float] = None
    year_built: Optional[int] = None
    price: Optional[float] = None
    listing_price: Optional[float] = None
    market_value: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    features: Optional[Dict[str, Any]] = None
    days_on_market: Optional[int] = None
    price_per_sqft: Optional[float] = None
    property_tax: Optional[float] = None
    hoa_fees: Optional[float] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class PropertyInDB(PropertyBase):
    """Property in database model."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PropertyResponse(PropertyBase):
    """Property response model."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
