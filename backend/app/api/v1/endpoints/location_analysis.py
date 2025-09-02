"""
Location analysis endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.location_analysis import LocationAnalysis, LocationAnalysisCreate, LocationAnalysisUpdate, LocationAnalysisResponse
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("location_analysis_endpoints")


@router.post("/", response_model=LocationAnalysisResponse)
async def create_location_analysis(
    analysis_data: LocationAnalysisCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new location analysis."""
    try:
        db_analysis = LocationAnalysis(**analysis_data.dict())
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)

        logger.info(f"Location analysis created: {analysis_data.location}")

        return LocationAnalysisResponse(
            id=db_analysis.id,
            location=db_analysis.location,
            safety_rating=db_analysis.safety_rating,
            schools=db_analysis.schools,
            transport=db_analysis.transport,
            summary=db_analysis.summary,
            created_at=db_analysis.created_at
        )

    except Exception as e:
        logger.error(f"Error creating location analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating location analysis"
        )


@router.get("/", response_model=List[LocationAnalysisResponse])
async def get_location_analyses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of location analyses."""
    try:
        analyses = db.query(LocationAnalysis).offset(skip).limit(limit).all()

        return [
            LocationAnalysisResponse(
                id=analysis.id,
                location=analysis.location,
                safety_rating=analysis.safety_rating,
                schools=analysis.schools,
                transport=analysis.transport,
                summary=analysis.summary,
                created_at=analysis.created_at
            )
            for analysis in analyses
        ]

    except Exception as e:
        logger.error(f"Error getting location analyses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving location analyses"
        )


@router.get("/{analysis_id}", response_model=LocationAnalysisResponse)
async def get_location_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific location analysis by ID."""
    try:
        analysis = db.query(LocationAnalysis).filter(LocationAnalysis.id == analysis_id).first()
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location analysis not found"
            )

        return LocationAnalysisResponse(
            id=analysis.id,
            location=analysis.location,
            safety_rating=analysis.safety_rating,
            schools=analysis.schools,
            transport=analysis.transport,
            summary=analysis.summary,
            created_at=analysis.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting location analysis {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving location analysis"
        )


@router.put("/{analysis_id}", response_model=LocationAnalysisResponse)
async def update_location_analysis(
    analysis_id: int,
    analysis_data: LocationAnalysisUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a location analysis."""
    try:
        analysis = db.query(LocationAnalysis).filter(LocationAnalysis.id == analysis_id).first()
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location analysis not found"
            )

        # Update only provided fields
        update_data = analysis_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(analysis, field, value)

        db.commit()
        db.refresh(analysis)

        logger.info(f"Location analysis updated: {analysis_id}")

        return LocationAnalysisResponse(
            id=analysis.id,
            location=analysis.location,
            safety_rating=analysis.safety_rating,
            schools=analysis.schools,
            transport=analysis.transport,
            summary=analysis.summary,
            created_at=analysis.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating location analysis {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating location analysis"
        )


@router.delete("/{analysis_id}")
async def delete_location_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a location analysis."""
    try:
        analysis = db.query(LocationAnalysis).filter(LocationAnalysis.id == analysis_id).first()
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location analysis not found"
            )

        db.delete(analysis)
        db.commit()

        logger.info(f"Location analysis deleted: {analysis_id}")

        return {"message": "Location analysis deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting location analysis {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting location analysis"
        )
