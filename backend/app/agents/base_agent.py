"""
Base agent class for all AI agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import uuid
from enum import Enum

from app.core.logging import get_logger
from app.core.config import settings


class AgentStatus(Enum):
    """Agent status enumeration."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class CommunicationProtocol(Enum):
    """Communication protocol enumeration."""
    REST_API = "rest_api"
    WEBSOCKET = "websocket"
    INTERNAL = "internal"


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(self, agent_name: str, agent_type: str):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.agent_id = str(uuid.uuid4())
        self.status = AgentStatus.IDLE
        self.logger = get_logger(f"agent.{agent_name}")
        
        # Performance tracking
        self.processing_time = 0.0
        self.memory_usage = 0.0
        self.cpu_usage = 0.0
        
        # Communication
        self.communication_protocol = CommunicationProtocol.INTERNAL
        self.message_queue = asyncio.Queue()
        self.active_tasks = []
        
        self.logger.info(f"Agent {agent_name} initialized with ID {self.agent_id}")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results."""
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        pass
    
    async def startup(self):
        """Startup the agent."""
        self.status = AgentStatus.IDLE
        self.logger.info(f"Agent {self.agent_name} started")
    
    async def shutdown(self):
        """Shutdown the agent."""
        self.status = AgentStatus.OFFLINE
        # Cancel all active tasks
        for task in self.active_tasks:
            if not task.done():
                task.cancel()
        self.logger.info(f"Agent {self.agent_name} shutdown")
    
    async def send_message(self, target_agent: str, message: Dict[str, Any]) -> bool:
        """Send message to another agent."""
        try:
            message_id = str(uuid.uuid4())
            message_data = {
                "message_id": message_id,
                "from_agent": self.agent_name,
                "to_agent": target_agent,
                "timestamp": datetime.utcnow().isoformat(),
                "data": message
            }
            
            self.logger.info(f"Sending message {message_id} to {target_agent}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message to {target_agent}: {e}")
            return False
    
    async def receive_message(self, message: Dict[str, Any]) -> bool:
        """Receive message from another agent."""
        try:
            self.logger.info(f"Received message from {message.get('from_agent')}")
            await self.message_queue.put(message)
            return True
        except Exception as e:
            self.logger.error(f"Failed to receive message: {e}")
            return False
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "processing_time": self.processing_time,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "queue_size": self.message_queue.qsize(),
            "active_tasks": len(self.active_tasks)
        }
    
    def update_performance_metrics(self, processing_time: float, memory_usage: float, cpu_usage: float):
        """Update performance metrics."""
        self.processing_time = processing_time
        self.memory_usage = memory_usage
        self.cpu_usage = cpu_usage
    
    async def handle_error(self, error: Exception, context: str = ""):
        """Handle agent errors."""
        self.status = AgentStatus.ERROR
        self.logger.error(f"Agent {self.agent_name} error in {context}: {error}")
        
        # In a real system, you might want to:
        # - Send error notifications
        # - Retry the operation
        # - Fall back to alternative processing
        # - Update monitoring systems
    
    async def retry_operation(self, operation, max_retries: int = 3, delay: float = 1.0):
        """Retry an operation with exponential backoff."""
        for attempt in range(max_retries):
            try:
                return await operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                wait_time = delay * (2 ** attempt)
                self.logger.warning(f"Operation failed, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                await asyncio.sleep(wait_time)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.agent_name}', status='{self.status.value}')>"
