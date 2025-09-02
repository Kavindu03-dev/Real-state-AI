"""
Main FastAPI application for the Real Estate AI system.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.security import get_current_user, User
from app.api.v1.api import api_router
from app.core.database import init_db
from app.core.logging import setup_logging
from app.agents.orchestrator import AgentOrchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging()
    await init_db()
    app.state.orchestrator = AgentOrchestrator()
    await app.state.orchestrator.startup()
    
    yield
    
    # Shutdown
    await app.state.orchestrator.shutdown()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-Agent AI System for Real Estate Analysis",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Security middleware
security = HTTPBearer()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Real Estate AI - Multi-Agent System",
        "version": settings.APP_VERSION,
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agents": {
            "price_estimator": "active",
            "location_analyzer": "active", 
            "deal_evaluator": "active"
        }
    }


@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    """Protected route example."""
    return {"message": "This is a protected route", "user": current_user.email}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS
    )
