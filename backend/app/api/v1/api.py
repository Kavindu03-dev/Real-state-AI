"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, properties, location_analysis, deal_evaluations

api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(location_analysis.router, prefix="/location-analysis", tags=["location-analysis"])
api_router.include_router(deal_evaluations.router, prefix="/deal-evaluations", tags=["deal-evaluations"])
