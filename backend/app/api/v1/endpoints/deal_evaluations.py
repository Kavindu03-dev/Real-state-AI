"""
Deal evaluation endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.deal_evaluation import DealEvaluation, DealEvaluationCreate, DealEvaluationUpdate, DealEvaluationResponse
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("deal_evaluation_endpoints")


@router.post("/", response_model=DealEvaluationResponse)
async def create_deal_evaluation(
    evaluation_data: DealEvaluationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new deal evaluation."""
    try:
        # Check if property exists
        from app.models.property import Property
        property_obj = db.query(Property).filter(Property.id == evaluation_data.property_id).first()
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )

        db_evaluation = DealEvaluation(**evaluation_data.dict())
        db.add(db_evaluation)
        db.commit()
        db.refresh(db_evaluation)

        logger.info(f"Deal evaluation created for property: {evaluation_data.property_id}")

        return DealEvaluationResponse(
            id=db_evaluation.id,
            property_id=db_evaluation.property_id,
            deal_score=db_evaluation.deal_score,
            confidence=db_evaluation.confidence,
            explanation=db_evaluation.explanation,
            created_at=db_evaluation.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating deal evaluation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating deal evaluation"
        )


@router.get("/", response_model=List[DealEvaluationResponse])
async def get_deal_evaluations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of deal evaluations."""
    try:
        evaluations = db.query(DealEvaluation).offset(skip).limit(limit).all()

        return [
            DealEvaluationResponse(
                id=evaluation.id,
                property_id=evaluation.property_id,
                deal_score=evaluation.deal_score,
                confidence=evaluation.confidence,
                explanation=evaluation.explanation,
                created_at=evaluation.created_at
            )
            for evaluation in evaluations
        ]

    except Exception as e:
        logger.error(f"Error getting deal evaluations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving deal evaluations"
        )


@router.get("/{evaluation_id}", response_model=DealEvaluationResponse)
async def get_deal_evaluation(
    evaluation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific deal evaluation by ID."""
    try:
        evaluation = db.query(DealEvaluation).filter(DealEvaluation.id == evaluation_id).first()
        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deal evaluation not found"
            )

        return DealEvaluationResponse(
            id=evaluation.id,
            property_id=evaluation.property_id,
            deal_score=evaluation.deal_score,
            confidence=evaluation.confidence,
            explanation=evaluation.explanation,
            created_at=evaluation.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting deal evaluation {evaluation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving deal evaluation"
        )


@router.put("/{evaluation_id}", response_model=DealEvaluationResponse)
async def update_deal_evaluation(
    evaluation_id: int,
    evaluation_data: DealEvaluationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a deal evaluation."""
    try:
        evaluation = db.query(DealEvaluation).filter(DealEvaluation.id == evaluation_id).first()
        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deal evaluation not found"
            )

        # Update only provided fields
        update_data = evaluation_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(evaluation, field, value)

        db.commit()
        db.refresh(evaluation)

        logger.info(f"Deal evaluation updated: {evaluation_id}")

        return DealEvaluationResponse(
            id=evaluation.id,
            property_id=evaluation.property_id,
            deal_score=evaluation.deal_score,
            confidence=evaluation.confidence,
            explanation=evaluation.explanation,
            created_at=evaluation.created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating deal evaluation {evaluation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating deal evaluation"
        )


@router.delete("/{evaluation_id}")
async def delete_deal_evaluation(
    evaluation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a deal evaluation."""
    try:
        evaluation = db.query(DealEvaluation).filter(DealEvaluation.id == evaluation_id).first()
        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deal evaluation not found"
            )

        db.delete(evaluation)
        db.commit()

        logger.info(f"Deal evaluation deleted: {evaluation_id}")

        return {"message": "Deal evaluation deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting deal evaluation {evaluation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting deal evaluation"
        )
