"""
Central Orchestrator - Manages agent communication and coordinates analysis workflows.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from app.agents.base_agent import BaseAgent, AgentStatus
from app.agents.price_estimator import PriceEstimatorAgent
from app.agents.location_analyzer import LocationAnalyzerAgent
from app.agents.deal_evaluator import DealEvaluatorAgent
from app.core.logging import get_logger
from app.core.database import get_db
from app.models.analysis import Analysis, AnalysisCreate, AnalysisUpdate
from app.models.agent_log import AgentLog, AgentLogCreate


class AgentOrchestrator:
    """Central orchestrator for managing multi-agent communication and workflows."""
    
    def __init__(self):
        self.logger = get_logger("orchestrator")
        self.agents = {}
        self.workflows = {}
        self.message_queue = asyncio.Queue()
        self.is_running = False
        
    async def startup(self):
        """Initialize and start the orchestrator."""
        try:
            self.logger.info("Starting Agent Orchestrator")
            
            # Initialize agents
            await self._initialize_agents()
            
            # Start message processing
            self.is_running = True
            asyncio.create_task(self._process_messages())
            
            self.logger.info("Agent Orchestrator started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start orchestrator: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the orchestrator and all agents."""
        try:
            self.logger.info("Shutting down Agent Orchestrator")
            
            self.is_running = False
            
            # Shutdown all agents
            for agent in self.agents.values():
                await agent.shutdown()
            
            self.logger.info("Agent Orchestrator shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
    
    async def _initialize_agents(self):
        """Initialize all agents."""
        try:
            # Create agent instances
            self.agents["price_estimator"] = PriceEstimatorAgent()
            self.agents["location_analyzer"] = LocationAnalyzerAgent()
            self.agents["deal_evaluator"] = DealEvaluatorAgent()
            
            # Start all agents
            for name, agent in self.agents.items():
                await agent.startup()
                self.logger.info(f"Agent {name} initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing agents: {e}")
            raise
    
    async def _process_messages(self):
        """Process messages in the queue."""
        while self.is_running:
            try:
                # Get message from queue with timeout
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self._handle_message(message)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
    
    async def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming message."""
        try:
            message_type = message.get("type")
            target_agent = message.get("target_agent")
            
            if message_type == "analysis_request":
                await self._handle_analysis_request(message)
            elif message_type == "agent_communication":
                await self._handle_agent_communication(message)
            elif message_type == "status_request":
                await self._handle_status_request(message)
            else:
                self.logger.warning(f"Unknown message type: {message_type}")
                
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
    
    async def _handle_analysis_request(self, message: Dict[str, Any]):
        """Handle property analysis request."""
        try:
            workflow_id = str(uuid.uuid4())
            property_data = message.get("property_data", {})
            user_id = message.get("user_id")
            
            self.logger.info(f"Starting analysis workflow {workflow_id} for property")
            
            # Create analysis record
            analysis = await self._create_analysis_record(property_data, user_id, workflow_id)
            
            # Start workflow
            workflow_task = asyncio.create_task(
                self._execute_analysis_workflow(workflow_id, property_data, analysis.id)
            )
            
            self.workflows[workflow_id] = {
                "task": workflow_task,
                "status": "running",
                "start_time": datetime.utcnow(),
                "analysis_id": analysis.id
            }
            
        except Exception as e:
            self.logger.error(f"Error handling analysis request: {e}")
    
    async def _handle_agent_communication(self, message: Dict[str, Any]):
        """Handle inter-agent communication."""
        try:
            from_agent = message.get("from_agent")
            to_agent = message.get("to_agent")
            data = message.get("data", {})
            
            if to_agent in self.agents:
                await self.agents[to_agent].receive_message({
                    "from_agent": from_agent,
                    "data": data,
                    "timestamp": datetime.utcnow().isoformat()
                })
            else:
                self.logger.warning(f"Unknown target agent: {to_agent}")
                
        except Exception as e:
            self.logger.error(f"Error handling agent communication: {e}")
    
    async def _handle_status_request(self, message: Dict[str, Any]):
        """Handle status request."""
        try:
            agent_name = message.get("agent_name")
            
            if agent_name in self.agents:
                status = await self.agents[agent_name].get_status()
                # Send status response (implement response mechanism)
                self.logger.info(f"Agent {agent_name} status: {status}")
            else:
                self.logger.warning(f"Unknown agent: {agent_name}")
                
        except Exception as e:
            self.logger.error(f"Error handling status request: {e}")
    
    async def _execute_analysis_workflow(self, workflow_id: str, property_data: Dict[str, Any], analysis_id: int):
        """Execute the complete analysis workflow."""
        try:
            self.logger.info(f"Executing workflow {workflow_id}")
            
            # Step 1: Price Estimation
            price_result = await self._execute_price_estimation(property_data, analysis_id)
            
            # Step 2: Location Analysis
            location_result = await self._execute_location_analysis(property_data, analysis_id)
            
            # Step 3: Deal Evaluation
            deal_result = await self._execute_deal_evaluation(
                property_data, price_result, location_result, analysis_id
            )
            
            # Step 4: Combine Results
            combined_result = await self._combine_analysis_results(
                price_result, location_result, deal_result
            )
            
            # Step 5: Update Analysis Record
            await self._update_analysis_record(analysis_id, combined_result)
            
            # Mark workflow as complete
            self.workflows[workflow_id]["status"] = "completed"
            self.workflows[workflow_id]["end_time"] = datetime.utcnow()
            
            self.logger.info(f"Workflow {workflow_id} completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in workflow {workflow_id}: {e}")
            self.workflows[workflow_id]["status"] = "failed"
            self.workflows[workflow_id]["error"] = str(e)
    
    async def _execute_price_estimation(self, property_data: Dict[str, Any], analysis_id: int) -> Dict[str, Any]:
        """Execute price estimation analysis."""
        try:
            agent = self.agents["price_estimator"]
            
            # Log start
            await self._log_agent_activity(analysis_id, "price_estimator", "started", property_data)
            
            # Execute analysis
            result = await agent.process(property_data)
            
            # Log completion
            await self._log_agent_activity(analysis_id, "price_estimator", "completed", result)
            
            return result
            
        except Exception as e:
            await self._log_agent_activity(analysis_id, "price_estimator", "failed", {"error": str(e)})
            raise
    
    async def _execute_location_analysis(self, property_data: Dict[str, Any], analysis_id: int) -> Dict[str, Any]:
        """Execute location analysis."""
        try:
            agent = self.agents["location_analyzer"]
            
            # Log start
            await self._log_agent_activity(analysis_id, "location_analyzer", "started", property_data)
            
            # Execute analysis
            result = await agent.process(property_data)
            
            # Log completion
            await self._log_agent_activity(analysis_id, "location_analyzer", "completed", result)
            
            return result
            
        except Exception as e:
            await self._log_agent_activity(analysis_id, "location_analyzer", "failed", {"error": str(e)})
            raise
    
    async def _execute_deal_evaluation(
        self, 
        property_data: Dict[str, Any], 
        price_result: Dict[str, Any], 
        location_result: Dict[str, Any], 
        analysis_id: int
    ) -> Dict[str, Any]:
        """Execute deal evaluation analysis."""
        try:
            agent = self.agents["deal_evaluator"]
            
            # Prepare input data
            input_data = {
                "property_data": property_data,
                "price_estimate": price_result.get("estimated_price", 0),
                "location_score": location_result.get("location_score", 5.0)
            }
            
            # Log start
            await self._log_agent_activity(analysis_id, "deal_evaluator", "started", input_data)
            
            # Execute analysis
            result = await agent.process(input_data)
            
            # Log completion
            await self._log_agent_activity(analysis_id, "deal_evaluator", "completed", result)
            
            return result
            
        except Exception as e:
            await self._log_agent_activity(analysis_id, "deal_evaluator", "failed", {"error": str(e)})
            raise
    
    async def _combine_analysis_results(
        self, 
        price_result: Dict[str, Any], 
        location_result: Dict[str, Any], 
        deal_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine results from all agents."""
        try:
            # Calculate combined score
            price_score = min(price_result.get("confidence_score", 0.5) * 10, 10.0)
            location_score = location_result.get("location_score", 5.0)
            deal_score = deal_result.get("deal_score", 5.0)
            
            # Weighted average
            combined_score = (price_score * 0.3) + (location_score * 0.3) + (deal_score * 0.4)
            
            # Generate recommendations
            recommendations = []
            if deal_score >= 8.0:
                recommendations.append("Strong investment opportunity")
            elif deal_score >= 6.0:
                recommendations.append("Good investment potential")
            elif deal_score >= 4.0:
                recommendations.append("Moderate investment potential")
            else:
                recommendations.append("Limited investment potential")
            
            return {
                "combined_score": combined_score,
                "price_estimation": price_result,
                "location_analysis": location_result,
                "deal_evaluation": deal_result,
                "recommendations": recommendations,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error combining results: {e}")
            return {
                "combined_score": 5.0,
                "error": "Failed to combine analysis results"
            }
    
    async def _create_analysis_record(self, property_data: Dict[str, Any], user_id: int, workflow_id: str) -> Analysis:
        """Create analysis record in database."""
        try:
            db = next(get_db())
            
            analysis_data = AnalysisCreate(
                property_id=property_data.get("property_id", 0),
                user_id=user_id,
                analysis_type="comprehensive",
                status="processing"
            )
            
            analysis = Analysis(**analysis_data.dict())
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error creating analysis record: {e}")
            raise
    
    async def _update_analysis_record(self, analysis_id: int, result: Dict[str, Any]):
        """Update analysis record with results."""
        try:
            db = next(get_db())
            
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = "completed"
                analysis.price_estimator_result = result.get("price_estimation")
                analysis.location_analyzer_result = result.get("location_analysis")
                analysis.deal_evaluator_result = result.get("deal_evaluation")
                analysis.combined_score = result.get("combined_score")
                analysis.recommendations = result.get("recommendations")
                analysis.completed_at = datetime.utcnow()
                
                db.commit()
                
        except Exception as e:
            self.logger.error(f"Error updating analysis record: {e}")
    
    async def _log_agent_activity(self, analysis_id: int, agent_name: str, status: str, data: Dict[str, Any]):
        """Log agent activity."""
        try:
            db = next(get_db())
            
            log_data = AgentLogCreate(
                analysis_id=analysis_id,
                agent_name=agent_name,
                agent_type="llm",
                action="analysis",
                status=status,
                input_data=data if status == "started" else None,
                output_data=data if status == "completed" else None,
                error_message=data.get("error") if status == "failed" else None
            )
            
            log = AgentLog(**log_data.dict())
            db.add(log)
            db.commit()
            
        except Exception as e:
            self.logger.error(f"Error logging agent activity: {e}")
    
    async def get_agent_status(self, agent_name: str = None) -> Dict[str, Any]:
        """Get status of agents."""
        try:
            if agent_name:
                if agent_name in self.agents:
                    return await self.agents[agent_name].get_status()
                else:
                    return {"error": f"Agent {agent_name} not found"}
            
            # Return status of all agents
            status = {}
            for name, agent in self.agents.items():
                status[name] = await agent.get_status()
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting agent status: {e}")
            return {"error": str(e)}
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a specific workflow."""
        try:
            if workflow_id in self.workflows:
                workflow = self.workflows[workflow_id]
                return {
                    "workflow_id": workflow_id,
                    "status": workflow["status"],
                    "start_time": workflow["start_time"],
                    "end_time": workflow.get("end_time"),
                    "analysis_id": workflow["analysis_id"],
                    "error": workflow.get("error")
                }
            else:
                return {"error": f"Workflow {workflow_id} not found"}
                
        except Exception as e:
            self.logger.error(f"Error getting workflow status: {e}")
            return {"error": str(e)}
    
    async def submit_analysis_request(self, property_data: Dict[str, Any], user_id: int) -> str:
        """Submit a new analysis request."""
        try:
            workflow_id = str(uuid.uuid4())
            
            message = {
                "type": "analysis_request",
                "workflow_id": workflow_id,
                "property_data": property_data,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.message_queue.put(message)
            
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"Error submitting analysis request: {e}")
            raise
