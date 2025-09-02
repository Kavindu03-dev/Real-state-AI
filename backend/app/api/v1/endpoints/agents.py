"""
Agents endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Dict, Any

from app.core.security import get_current_active_user
from app.models.user import User
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger("agents_endpoints")


@router.get("/status")
async def get_agents_status(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get status of all agents."""
    try:
        orchestrator = request.app.state.orchestrator
        status_info = await orchestrator.get_agent_status()
        
        return {
            "agents": status_info,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving agents status"
        )


@router.get("/status/{agent_name}")
async def get_agent_status(
    agent_name: str,
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get status of a specific agent."""
    try:
        orchestrator = request.app.state.orchestrator
        status_info = await orchestrator.get_agent_status(agent_name)
        
        return {
            "agent": status_info,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error getting agent {agent_name} status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving agent status"
        )


@router.post("/restart/{agent_name}")
async def restart_agent(
    agent_name: str,
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Restart a specific agent."""
    try:
        # This would restart the agent in a real implementation
        # For now, return a mock response
        
        logger.info(f"Agent restart requested: {agent_name} by user {current_user.id}")
        
        return {
            "message": f"Agent {agent_name} restart initiated",
            "status": "restarting",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error restarting agent {agent_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error restarting agent"
        )


@router.get("/metrics")
async def get_agents_metrics(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get performance metrics for all agents."""
    try:
        # Mock metrics data
        metrics = {
            "price_estimator": {
                "requests_processed": 150,
                "average_response_time": 2.5,
                "success_rate": 0.95,
                "memory_usage": "45MB",
                "cpu_usage": "12%"
            },
            "location_analyzer": {
                "requests_processed": 120,
                "average_response_time": 3.2,
                "success_rate": 0.92,
                "memory_usage": "38MB",
                "cpu_usage": "15%"
            },
            "deal_evaluator": {
                "requests_processed": 80,
                "average_response_time": 4.1,
                "success_rate": 0.88,
                "memory_usage": "52MB",
                "cpu_usage": "18%"
            }
        }
        
        return {
            "metrics": metrics,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error getting agents metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving agents metrics"
        )


@router.get("/logs")
async def get_agents_logs(
    agent_name: str = None,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user)
):
    """Get recent logs from agents."""
    try:
        # Mock log data
        logs = [
            {
                "timestamp": "2024-01-01T10:30:00Z",
                "agent": "price_estimator",
                "level": "INFO",
                "message": "Processing price estimation request"
            },
            {
                "timestamp": "2024-01-01T10:29:00Z",
                "agent": "location_analyzer",
                "level": "INFO",
                "message": "Location analysis completed"
            },
            {
                "timestamp": "2024-01-01T10:28:00Z",
                "agent": "deal_evaluator",
                "level": "WARNING",
                "message": "Low confidence in deal evaluation"
            }
        ]
        
        if agent_name:
            logs = [log for log in logs if log["agent"] == agent_name]
        
        return {
            "logs": logs[:limit],
            "total": len(logs),
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error getting agents logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving agents logs"
        )


@router.post("/test")
async def test_agent(
    agent_name: str,
    test_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    request: Request = None
):
    """Test a specific agent with sample data."""
    try:
        # Mock test response
        test_results = {
            "agent": agent_name,
            "status": "success",
            "response_time": 1.5,
            "result": {
                "test_data": test_data,
                "processed": True,
                "confidence": 0.85
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        logger.info(f"Agent test performed: {agent_name} by user {current_user.id}")
        
        return test_results
        
    except Exception as e:
        logger.error(f"Error testing agent {agent_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error testing agent"
        )


@router.get("/health")
async def get_system_health(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get overall system health status."""
    try:
        # Mock health check
        health_status = {
            "status": "healthy",
            "agents": {
                "price_estimator": "active",
                "location_analyzer": "active",
                "deal_evaluator": "active"
            },
            "database": "connected",
            "redis": "connected",
            "external_apis": "available",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        return health_status
        
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving system health"
        )
