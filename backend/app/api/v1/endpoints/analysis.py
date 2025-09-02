"""
Analysis endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.analysis import Analysis, AnalysisCreate, AnalysisResponse
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("analysis_endpoints")


@router.post("/property", response_model=Dict[str, Any])
async def analyze_property(
    request: Request,
    property_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit a property for comprehensive analysis."""
    try:
        # Get orchestrator from app state
        orchestrator = request.app.state.orchestrator
        
        # Submit analysis request
        workflow_id = await orchestrator.submit_analysis_request(property_data, current_user.id)
        
        logger.info(f"Analysis requested for property by user {current_user.id}, workflow: {workflow_id}")
        
        return {
            "workflow_id": workflow_id,
            "status": "processing",
            "message": "Analysis request submitted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error submitting analysis request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error submitting analysis request"
        )


@router.get("/status/{workflow_id}")
async def get_analysis_status(
    workflow_id: str,
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get the status of an analysis workflow."""
    try:
        orchestrator = request.app.state.orchestrator
        status_info = await orchestrator.get_workflow_status(workflow_id)
        
        return status_info
        
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving workflow status"
        )


@router.get("/", response_model=List[AnalysisResponse])
async def get_analyses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of analyses for the current user."""
    try:
        analyses = db.query(Analysis).filter(
            Analysis.user_id == current_user.id
        ).offset(skip).limit(limit).all()
        
        return [
            AnalysisResponse(
                id=analysis.id,
                property_id=analysis.property_id,
                analysis_type=analysis.analysis_type,
                status=analysis.status,
                price_estimator_result=analysis.price_estimator_result,
                location_analyzer_result=analysis.location_analyzer_result,
                deal_evaluator_result=analysis.deal_evaluator_result,
                combined_score=analysis.combined_score,
                confidence_level=analysis.confidence_level,
                recommendations=analysis.recommendations,
                created_at=analysis.created_at,
                completed_at=analysis.completed_at
            )
            for analysis in analyses
        ]
        
    except Exception as e:
        logger.error(f"Error getting analyses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving analyses"
        )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific analysis by ID."""
    try:
        analysis = db.query(Analysis).filter(
            Analysis.id == analysis_id,
            Analysis.user_id == current_user.id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        return AnalysisResponse(
            id=analysis.id,
            property_id=analysis.property_id,
            analysis_type=analysis.analysis_type,
            status=analysis.status,
            price_estimator_result=analysis.price_estimator_result,
            location_analyzer_result=analysis.location_analyzer_result,
            deal_evaluator_result=analysis.deal_evaluator_result,
            combined_score=analysis.combined_score,
            confidence_level=analysis.confidence_level,
            recommendations=analysis.recommendations,
            created_at=analysis.created_at,
            completed_at=analysis.completed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis {analysis_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving analysis"
        )


@router.post("/quick-price")
async def quick_price_estimate(
    property_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    request: Request = None
):
    """Get a quick price estimate for a property."""
    try:
        # This would use a simplified version of the price estimator
        # For now, return a mock response
        estimated_price = 425000  # Mock price
        
        return {
            "estimated_price": estimated_price,
            "confidence": 0.75,
            "method": "quick_estimate",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error in quick price estimate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error calculating price estimate"
        )


@router.post("/location-score")
async def get_location_score(
    location_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user)
):
    """Get a location score for a property."""
    try:
        # Mock location score calculation
        location_score = 7.5  # Mock score
        
        return {
            "location_score": location_score,
            "factors": ["good schools", "low crime", "convenient amenities"],
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error calculating location score: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error calculating location score"
        )


@router.post("/deal-evaluation")
async def evaluate_deal(
    deal_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user)
):
    """Evaluate a real estate deal."""
    try:
        # Mock deal evaluation
        deal_score = 6.8  # Mock score
        
        return {
            "deal_score": deal_score,
            "roi_estimate": 0.065,
            "risk_level": "medium",
            "recommendation": "consider",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error evaluating deal: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error evaluating deal"
        )
