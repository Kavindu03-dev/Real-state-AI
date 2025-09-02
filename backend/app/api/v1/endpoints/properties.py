"""
Properties endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.property import Property, PropertyCreate, PropertyUpdate, PropertyResponse
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("properties_endpoints")


@router.post("/", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new property."""
    try:
        db_property = Property(**property_data.dict())
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        
        logger.info(f"Property created: {property_data.address}")
        
        return PropertyResponse(
            id=db_property.id,
            address=db_property.address,
            city=db_property.city,
            state=db_property.state,
            zip_code=db_property.zip_code,
            property_type=db_property.property_type,
            bedrooms=db_property.bedrooms,
            bathrooms=db_property.bathrooms,
            square_feet=db_property.square_feet,
            lot_size=db_property.lot_size,
            year_built=db_property.year_built,
            price=db_property.price,
            listing_price=db_property.listing_price,
            market_value=db_property.market_value,
            latitude=db_property.latitude,
            longitude=db_property.longitude,
            features=db_property.features,
            days_on_market=db_property.days_on_market,
            price_per_sqft=db_property.price_per_sqft,
            property_tax=db_property.property_tax,
            hoa_fees=db_property.hoa_fees,
            status=db_property.status,
            is_active=db_property.is_active,
            created_at=db_property.created_at
        )
        
    except Exception as e:
        logger.error(f"Error creating property: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating property"
        )


@router.get("/", response_model=List[PropertyResponse])
async def get_properties(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of properties."""
    try:
        properties = db.query(Property).filter(Property.is_active == True).offset(skip).limit(limit).all()
        
        return [
            PropertyResponse(
                id=prop.id,
                address=prop.address,
                city=prop.city,
                state=prop.state,
                zip_code=prop.zip_code,
                property_type=prop.property_type,
                bedrooms=prop.bedrooms,
                bathrooms=prop.bathrooms,
                square_feet=prop.square_feet,
                lot_size=prop.lot_size,
                year_built=prop.year_built,
                price=prop.price,
                listing_price=prop.listing_price,
                market_value=prop.market_value,
                latitude=prop.latitude,
                longitude=prop.longitude,
                features=prop.features,
                days_on_market=prop.days_on_market,
                price_per_sqft=prop.price_per_sqft,
                property_tax=prop.property_tax,
                hoa_fees=prop.hoa_fees,
                status=prop.status,
                is_active=prop.is_active,
                created_at=prop.created_at
            )
            for prop in properties
        ]
        
    except Exception as e:
        logger.error(f"Error getting properties: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving properties"
        )


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific property by ID."""
    try:
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        
        return PropertyResponse(
            id=property_obj.id,
            address=property_obj.address,
            city=property_obj.city,
            state=property_obj.state,
            zip_code=property_obj.zip_code,
            property_type=property_obj.property_type,
            bedrooms=property_obj.bedrooms,
            bathrooms=property_obj.bathrooms,
            square_feet=property_obj.square_feet,
            lot_size=property_obj.lot_size,
            year_built=property_obj.year_built,
            price=property_obj.price,
            listing_price=property_obj.listing_price,
            market_value=property_obj.market_value,
            latitude=property_obj.latitude,
            longitude=property_obj.longitude,
            features=property_obj.features,
            days_on_market=property_obj.days_on_market,
            price_per_sqft=property_obj.price_per_sqft,
            property_tax=property_obj.property_tax,
            hoa_fees=property_obj.hoa_fees,
            status=property_obj.status,
            is_active=property_obj.is_active,
            created_at=property_obj.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting property {property_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving property"
        )


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a property."""
    try:
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        
        # Update only provided fields
        update_data = property_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(property_obj, field, value)
        
        db.commit()
        db.refresh(property_obj)
        
        logger.info(f"Property updated: {property_id}")
        
        return PropertyResponse(
            id=property_obj.id,
            address=property_obj.address,
            city=property_obj.city,
            state=property_obj.state,
            zip_code=property_obj.zip_code,
            property_type=property_obj.property_type,
            bedrooms=property_obj.bedrooms,
            bathrooms=property_obj.bathrooms,
            square_feet=property_obj.square_feet,
            lot_size=property_obj.lot_size,
            year_built=property_obj.year_built,
            price=property_obj.price,
            listing_price=property_obj.listing_price,
            market_value=property_obj.market_value,
            latitude=property_obj.latitude,
            longitude=property_obj.longitude,
            features=property_obj.features,
            days_on_market=property_obj.days_on_market,
            price_per_sqft=property_obj.price_per_sqft,
            property_tax=property_obj.property_tax,
            hoa_fees=property_obj.hoa_fees,
            status=property_obj.status,
            is_active=property_obj.is_active,
            created_at=property_obj.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating property {property_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating property"
        )


@router.delete("/{property_id}")
async def delete_property(
    property_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a property (soft delete)."""
    try:
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        
        # Soft delete
        property_obj.is_active = False
        db.commit()
        
        logger.info(f"Property deleted: {property_id}")
        
        return {"message": "Property deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting property {property_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting property"
        )
