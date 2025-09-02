"""
Deal Evaluator Agent - Assesses investment potential and deal attractiveness.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.agents.base_agent import BaseAgent
from app.core.logging import get_logger
from app.services.llm_service import LLMService
from app.services.data_service import DataService


class DealEvaluatorAgent(BaseAgent):
    """Deal Evaluator Agent for investment analysis."""
    
    def __init__(self):
        super().__init__("deal_evaluator", "llm")
        self.llm_service = LLMService()
        self.data_service = DataService()
        self.logger = get_logger("agent.deal_evaluator")
        
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for deal evaluation."""
        required_fields = ["property_data", "price_estimate", "location_score"]
        
        for field in required_fields:
            if field not in input_data or input_data[field] is None:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process deal data and evaluate investment potential."""
        start_time = time.time()
        self.status.value = "busy"
        
        try:
            if not await self.validate_input(input_data):
                raise ValueError("Invalid input data")
            
            self.logger.info(f"Processing deal evaluation for property")
            
            # Extract data
            property_data = input_data["property_data"]
            price_estimate = input_data["price_estimate"]
            location_score = input_data["location_score"]
            
            # Calculate ROI metrics
            roi_metrics = await self._calculate_roi_metrics(property_data, price_estimate)
            
            # Assess market timing
            market_timing = await self._assess_market_timing(property_data)
            
            # Evaluate risk factors
            risk_assessment = await self._evaluate_risks(property_data, price_estimate, location_score)
            
            # Calculate deal score
            deal_score = await self._calculate_deal_score(roi_metrics, market_timing, risk_assessment)
            
            # Generate investment strategy
            strategy = await self._generate_investment_strategy(deal_score, roi_metrics, risk_assessment)
            
            # Generate detailed analysis
            analysis = await self._generate_deal_analysis(property_data, deal_score, roi_metrics, strategy)
            
            processing_time = time.time() - start_time
            self.update_performance_metrics(processing_time, 0.0, 0.0)
            
            result = {
                "deal_score": deal_score,
                "roi_metrics": roi_metrics,
                "market_timing": market_timing,
                "risk_assessment": risk_assessment,
                "investment_strategy": strategy,
                "analysis": analysis,
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.logger.info(f"Deal evaluation completed: Score {deal_score:.2f}/10")
            return result
            
        except Exception as e:
            await self.handle_error(e, "deal_evaluation")
            raise
    
    async def _calculate_roi_metrics(self, property_data: Dict[str, Any], price_estimate: float) -> Dict[str, Any]:
        """Calculate ROI and investment metrics."""
        try:
            # Get rental data
            rental_data = await self.data_service.get_rental_data(
                city=property_data.get("city"),
                state=property_data.get("state"),
                bedrooms=property_data.get("bedrooms", 0)
            )
            
            # Calculate metrics
            monthly_rent = rental_data.get("avg_monthly_rent", price_estimate * 0.008)  # 0.8% rule
            annual_rent = monthly_rent * 12
            cap_rate = (annual_rent / price_estimate) * 100 if price_estimate > 0 else 0
            
            # Calculate cash flow
            property_tax = property_data.get("property_tax", price_estimate * 0.012)  # 1.2% of value
            insurance = price_estimate * 0.005  # 0.5% of value
            maintenance = annual_rent * 0.1  # 10% of rent
            hoa_fees = property_data.get("hoa_fees", 0) * 12
            
            total_expenses = property_tax + insurance + maintenance + hoa_fees
            net_operating_income = annual_rent - total_expenses
            
            # Calculate cash on cash return
            down_payment = price_estimate * 0.25  # 25% down
            closing_costs = price_estimate * 0.03  # 3% closing costs
            total_investment = down_payment + closing_costs
            
            cash_on_cash_return = (net_operating_income / total_investment) * 100 if total_investment > 0 else 0
            
            return {
                "monthly_rent": monthly_rent,
                "annual_rent": annual_rent,
                "cap_rate": cap_rate,
                "net_operating_income": net_operating_income,
                "cash_on_cash_return": cash_on_cash_return,
                "total_investment": total_investment,
                "expenses": {
                    "property_tax": property_tax,
                    "insurance": insurance,
                    "maintenance": maintenance,
                    "hoa_fees": hoa_fees,
                    "total": total_expenses
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating ROI metrics: {e}")
            return {
                "monthly_rent": 0,
                "annual_rent": 0,
                "cap_rate": 0,
                "net_operating_income": 0,
                "cash_on_cash_return": 0,
                "total_investment": 0,
                "expenses": {"total": 0}
            }
    
    async def _assess_market_timing(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess market timing for the investment."""
        try:
            # Get market data
            market_data = await self.data_service.get_market_data(
                city=property_data.get("city"),
                state=property_data.get("state")
            )
            
            # Analyze market timing
            price_trend = market_data.get("price_trend", "stable")
            inventory_level = market_data.get("inventory_level", 0)
            days_on_market = market_data.get("days_on_market", 30)
            
            # Calculate timing score
            timing_score = 5.0  # Base score
            
            if price_trend == "rising":
                timing_score += 2.0
            elif price_trend == "declining":
                timing_score -= 1.0
            
            if inventory_level < 3:  # Low inventory
                timing_score += 1.0
            elif inventory_level > 6:  # High inventory
                timing_score -= 1.0
            
            if days_on_market < 30:
                timing_score += 1.0
            elif days_on_market > 60:
                timing_score -= 1.0
            
            timing_score = max(0.0, min(10.0, timing_score))
            
            prompt = f"Assess market timing for {property_data.get('city')}: Trend {price_trend}, Inventory {inventory_level}, DOM {days_on_market}"
            analysis = await self.llm_service.generate_text(prompt)
            
            return {
                "price_trend": price_trend,
                "inventory_level": inventory_level,
                "days_on_market": days_on_market,
                "timing_score": timing_score,
                "analysis": analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing market timing: {e}")
            return {
                "price_trend": "unknown",
                "inventory_level": 0,
                "days_on_market": 0,
                "timing_score": 5.0,
                "analysis": "Unable to assess market timing"
            }
    
    async def _evaluate_risks(self, property_data: Dict[str, Any], price_estimate: float, location_score: float) -> Dict[str, Any]:
        """Evaluate investment risks."""
        try:
            risks = {
                "market_risk": "low",
                "property_risk": "low",
                "location_risk": "low",
                "financial_risk": "low",
                "overall_risk": "low"
            }
            
            # Market risk
            if price_estimate > 1000000:  # High-value property
                risks["market_risk"] = "medium"
            
            # Property risk
            year_built = property_data.get("year_built", 2000)
            if year_built < 1980:
                risks["property_risk"] = "medium"
            elif year_built < 1960:
                risks["property_risk"] = "high"
            
            # Location risk
            if location_score < 5.0:
                risks["location_risk"] = "high"
            elif location_score < 7.0:
                risks["location_risk"] = "medium"
            
            # Financial risk
            if price_estimate > 500000:  # High purchase price
                risks["financial_risk"] = "medium"
            
            # Overall risk assessment
            risk_levels = {"low": 1, "medium": 2, "high": 3}
            avg_risk = sum(risk_levels[risk] for risk in risks.values() if risk != "overall_risk") / 4
            
            if avg_risk <= 1.5:
                risks["overall_risk"] = "low"
            elif avg_risk <= 2.5:
                risks["overall_risk"] = "medium"
            else:
                risks["overall_risk"] = "high"
            
            prompt = f"Evaluate investment risks for property: Year built {year_built}, Location score {location_score}, Price ${price_estimate:,.0f}"
            analysis = await self.llm_service.generate_text(prompt)
            
            return {
                "risk_factors": risks,
                "analysis": analysis,
                "risk_score": 10.0 - (avg_risk * 2)  # Convert to 0-10 scale
            }
            
        except Exception as e:
            self.logger.error(f"Error evaluating risks: {e}")
            return {
                "risk_factors": {"overall_risk": "medium"},
                "analysis": "Unable to evaluate risks",
                "risk_score": 5.0
            }
    
    async def _calculate_deal_score(self, roi_metrics: Dict[str, Any], market_timing: Dict[str, Any], risk_assessment: Dict[str, Any]) -> float:
        """Calculate overall deal score."""
        try:
            # ROI component (40% weight)
            roi_score = min(roi_metrics.get("cash_on_cash_return", 0) / 10.0, 10.0)  # 10% CoC = perfect score
            
            # Market timing component (30% weight)
            timing_score = market_timing.get("timing_score", 5.0)
            
            # Risk component (30% weight)
            risk_score = risk_assessment.get("risk_score", 5.0)
            
            # Calculate weighted score
            deal_score = (roi_score * 0.4) + (timing_score * 0.3) + (risk_score * 0.3)
            
            return min(deal_score, 10.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating deal score: {e}")
            return 5.0
    
    async def _generate_investment_strategy(self, deal_score: float, roi_metrics: Dict[str, Any], risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate investment strategy recommendations."""
        try:
            strategy_type = "hold"
            if deal_score >= 8.0:
                strategy_type = "buy"
            elif deal_score >= 6.0:
                strategy_type = "consider"
            elif deal_score < 4.0:
                strategy_type = "avoid"
            
            # Generate strategy details
            prompt = f"""
            Generate investment strategy for deal score {deal_score:.1f}/10:
            - Cash on cash return: {roi_metrics.get('cash_on_cash_return', 0):.1f}%
            - Risk level: {risk_assessment.get('risk_factors', {}).get('overall_risk', 'medium')}
            - Strategy type: {strategy_type}
            
            Provide specific recommendations for this investment opportunity.
            """
            
            strategy_analysis = await self.llm_service.generate_text(prompt)
            
            return {
                "strategy_type": strategy_type,
                "recommendations": self._get_strategy_recommendations(strategy_type, deal_score),
                "analysis": strategy_analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error generating investment strategy: {e}")
            return {
                "strategy_type": "hold",
                "recommendations": ["Evaluate carefully"],
                "analysis": "Unable to generate strategy"
            }
    
    async def _generate_deal_analysis(self, property_data: Dict[str, Any], deal_score: float, roi_metrics: Dict[str, Any], strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive deal analysis."""
        try:
            prompt = f"""
            Generate comprehensive deal analysis for property:
            - Address: {property_data.get('address')}
            - Deal Score: {deal_score:.1f}/10
            - Cash on Cash Return: {roi_metrics.get('cash_on_cash_return', 0):.1f}%
            - Strategy: {strategy.get('strategy_type', 'hold')}
            
            Provide detailed analysis including:
            1. Investment summary
            2. Financial projections
            3. Risk assessment
            4. Exit strategies
            5. Final recommendation
            """
            
            analysis = await self.llm_service.generate_text(prompt)
            
            return {
                "summary": analysis,
                "key_metrics": {
                    "deal_score": deal_score,
                    "cash_on_cash_return": roi_metrics.get("cash_on_cash_return", 0),
                    "cap_rate": roi_metrics.get("cap_rate", 0),
                    "total_investment": roi_metrics.get("total_investment", 0)
                },
                "recommendation": strategy.get("strategy_type", "hold")
            }
            
        except Exception as e:
            self.logger.error(f"Error generating deal analysis: {e}")
            return {
                "summary": "Analysis generation failed",
                "key_metrics": {},
                "recommendation": "hold"
            }
    
    def _get_strategy_recommendations(self, strategy_type: str, deal_score: float) -> List[str]:
        """Get strategy-specific recommendations."""
        recommendations = []
        
        if strategy_type == "buy":
            recommendations.extend([
                "Strong investment opportunity",
                "Consider making an offer",
                "Monitor market conditions",
                "Prepare financing options"
            ])
        elif strategy_type == "consider":
            recommendations.extend([
                "Moderate investment potential",
                "Negotiate for better terms",
                "Conduct thorough due diligence",
                "Consider alternative investments"
            ])
        elif strategy_type == "hold":
            recommendations.extend([
                "Wait for better market conditions",
                "Monitor for price changes",
                "Consider other properties",
                "Focus on portfolio optimization"
            ])
        else:  # avoid
            recommendations.extend([
                "Not recommended for investment",
                "Consider other opportunities",
                "Focus on different markets",
                "Reassess investment criteria"
            ])
        
        return recommendations
