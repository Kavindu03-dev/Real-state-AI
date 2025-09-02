"""
Price Estimator Agent - Analyzes property data to estimate market values.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
import numpy as np
from datetime import datetime

from app.agents.base_agent import BaseAgent
from app.core.logging import get_logger
from app.services.llm_service import LLMService
from app.services.data_service import DataService
from app.services.nlp_service import NLPService


class PriceEstimatorAgent(BaseAgent):
    """Price Estimator Agent for real estate valuation."""
    
    def __init__(self):
        super().__init__("price_estimator", "llm")
        self.llm_service = LLMService()
        self.data_service = DataService()
        self.nlp_service = NLPService()
        self.logger = get_logger("agent.price_estimator")
        
        # Model parameters
        self.confidence_threshold = 0.8
        self.max_comparables = 10
        
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for price estimation."""
        required_fields = ["address", "property_type", "bedrooms", "bathrooms", "square_feet"]
        
        for field in required_fields:
            if field not in input_data or input_data[field] is None:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Validate data types and ranges
        if not isinstance(input_data.get("bedrooms"), int) or input_data["bedrooms"] < 0:
            self.logger.error("Invalid bedrooms value")
            return False
        
        if not isinstance(input_data.get("bathrooms"), (int, float)) or input_data["bathrooms"] <= 0:
            self.logger.error("Invalid bathrooms value")
            return False
        
        if not isinstance(input_data.get("square_feet"), int) or input_data["square_feet"] <= 0:
            self.logger.error("Invalid square_feet value")
            return False
        
        return True
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process property data and estimate price."""
        start_time = time.time()
        self.status.value = "busy"
        
        try:
            # Validate input
            if not await self.validate_input(input_data):
                raise ValueError("Invalid input data")
            
            self.logger.info(f"Processing price estimation for {input_data.get('address')}")
            
            # Step 1: Gather comparable properties
            comparables = await self._get_comparable_properties(input_data)
            
            # Step 2: Analyze market trends
            market_trends = await self._analyze_market_trends(input_data)
            
            # Step 3: Extract features from property description
            features = await self._extract_property_features(input_data)
            
            # Step 4: Generate price estimate using LLM
            price_estimate = await self._generate_price_estimate(
                input_data, comparables, market_trends, features
            )
            
            # Step 5: Calculate confidence score
            confidence_score = await self._calculate_confidence(
                input_data, comparables, price_estimate
            )
            
            # Step 6: Generate detailed analysis
            analysis = await self._generate_detailed_analysis(
                input_data, comparables, market_trends, price_estimate, confidence_score
            )
            
            processing_time = time.time() - start_time
            self.update_performance_metrics(processing_time, 0.0, 0.0)
            
            result = {
                "estimated_price": price_estimate,
                "confidence_score": confidence_score,
                "comparables_used": len(comparables),
                "market_trends": market_trends,
                "property_features": features,
                "detailed_analysis": analysis,
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.logger.info(f"Price estimation completed: ${price_estimate:,.2f} (confidence: {confidence_score:.2f})")
            return result
            
        except Exception as e:
            await self.handle_error(e, "price_estimation")
            raise
    
    async def _get_comparable_properties(self, property_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get comparable properties from the database."""
        try:
            comparables = await self.data_service.get_comparable_properties(
                address=property_data["address"],
                property_type=property_data["property_type"],
                bedrooms=property_data["bedrooms"],
                bathrooms=property_data["bathrooms"],
                square_feet=property_data["square_feet"],
                limit=self.max_comparables
            )
            
            self.logger.info(f"Found {len(comparables)} comparable properties")
            return comparables
            
        except Exception as e:
            self.logger.error(f"Error getting comparable properties: {e}")
            return []
    
    async def _analyze_market_trends(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market trends for the area."""
        try:
            # Get market data for the area
            market_data = await self.data_service.get_market_data(
                city=property_data.get("city"),
                state=property_data.get("state"),
                zip_code=property_data.get("zip_code")
            )
            
            # Analyze trends using LLM
            trend_prompt = f"""
            Analyze the following market data for {property_data.get('city')}, {property_data.get('state')}:
            
            Market Data:
            - Average price: ${market_data.get('avg_price', 0):,.2f}
            - Price per sqft: ${market_data.get('price_per_sqft', 0):,.2f}
            - Days on market: {market_data.get('days_on_market', 0)}
            - Inventory level: {market_data.get('inventory_level', 0)}
            - Price trend: {market_data.get('price_trend', 'stable')}
            
            Provide a brief analysis of the market trends and their impact on property values.
            """
            
            trend_analysis = await self.llm_service.generate_text(trend_prompt)
            
            return {
                "market_data": market_data,
                "trend_analysis": trend_analysis,
                "trend_direction": market_data.get("price_trend", "stable")
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing market trends: {e}")
            return {"trend_analysis": "Unable to analyze market trends", "trend_direction": "unknown"}
    
    async def _extract_property_features(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and analyze property features from description."""
        try:
            description = property_data.get("description", "")
            if not description:
                return {"features": [], "feature_score": 0.0}
            
            # Use NLP to extract features
            features = await self.nlp_service.extract_property_features(description)
            
            # Calculate feature score
            feature_score = await self._calculate_feature_score(features)
            
            return {
                "features": features,
                "feature_score": feature_score
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting property features: {e}")
            return {"features": [], "feature_score": 0.0}
    
    async def _generate_price_estimate(
        self, 
        property_data: Dict[str, Any], 
        comparables: List[Dict[str, Any]], 
        market_trends: Dict[str, Any],
        features: Dict[str, Any]
    ) -> float:
        """Generate price estimate using LLM and comparable analysis."""
        try:
            # Prepare comparable data
            comp_data = []
            for comp in comparables[:5]:  # Use top 5 comparables
                comp_data.append({
                    "price": comp.get("price", 0),
                    "sqft": comp.get("square_feet", 0),
                    "bedrooms": comp.get("bedrooms", 0),
                    "bathrooms": comp.get("bathrooms", 0),
                    "days_on_market": comp.get("days_on_market", 0)
                })
            
            # Create LLM prompt
            prompt = f"""
            As a real estate price estimator, analyze the following property and provide a price estimate:
            
            Property Details:
            - Address: {property_data.get('address')}
            - Type: {property_data.get('property_type')}
            - Bedrooms: {property_data.get('bedrooms')}
            - Bathrooms: {property_data.get('bathrooms')}
            - Square Feet: {property_data.get('square_feet')}
            - Year Built: {property_data.get('year_built', 'Unknown')}
            
            Comparable Properties:
            {comp_data}
            
            Market Trends:
            {market_trends.get('trend_analysis', 'No trend data available')}
            
            Property Features:
            {features.get('features', [])}
            
            Based on this information, provide a single price estimate in USD (just the number, no formatting).
            Consider the comparables, market trends, and property features in your estimation.
            """
            
            # Get LLM response
            response = await self.llm_service.generate_text(prompt)
            
            # Extract price from response
            try:
                # Clean the response and extract numeric value
                price_str = ''.join(filter(str.isdigit, response))
                if price_str:
                    estimated_price = float(price_str)
                else:
                    # Fallback to comparable average
                    prices = [comp.get("price", 0) for comp in comparables if comp.get("price", 0) > 0]
                    estimated_price = sum(prices) / len(prices) if prices else 0
            except (ValueError, ZeroDivisionError):
                estimated_price = 0
            
            return estimated_price
            
        except Exception as e:
            self.logger.error(f"Error generating price estimate: {e}")
            # Fallback to simple calculation
            return self._calculate_fallback_price(property_data, comparables)
    
    async def _calculate_confidence(
        self, 
        property_data: Dict[str, Any], 
        comparables: List[Dict[str, Any]], 
        estimated_price: float
    ) -> float:
        """Calculate confidence score for the price estimate."""
        try:
            confidence_factors = []
            
            # Factor 1: Number of comparables
            comp_count = len(comparables)
            comp_confidence = min(comp_count / 5.0, 1.0)  # Max confidence with 5+ comparables
            confidence_factors.append(comp_confidence)
            
            # Factor 2: Price consistency among comparables
            if comparables:
                prices = [comp.get("price", 0) for comp in comparables if comp.get("price", 0) > 0]
                if prices:
                    price_std = np.std(prices)
                    price_mean = np.mean(prices)
                    price_cv = price_std / price_mean if price_mean > 0 else 1.0
                    price_confidence = max(0, 1 - price_cv)  # Lower CV = higher confidence
                    confidence_factors.append(price_confidence)
            
            # Factor 3: Data completeness
            required_fields = ["bedrooms", "bathrooms", "square_feet", "year_built"]
            completeness = sum(1 for field in required_fields if property_data.get(field) is not None) / len(required_fields)
            confidence_factors.append(completeness)
            
            # Factor 4: Market data availability
            market_confidence = 0.8 if len(comparables) > 0 else 0.3
            confidence_factors.append(market_confidence)
            
            # Calculate overall confidence
            overall_confidence = sum(confidence_factors) / len(confidence_factors)
            return min(overall_confidence, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            return 0.5  # Default confidence
    
    async def _generate_detailed_analysis(
        self,
        property_data: Dict[str, Any],
        comparables: List[Dict[str, Any]],
        market_trends: Dict[str, Any],
        estimated_price: float,
        confidence_score: float
    ) -> Dict[str, Any]:
        """Generate detailed analysis report."""
        try:
            analysis_prompt = f"""
            Generate a detailed real estate analysis report for the following property:
            
            Property: {property_data.get('address')}
            Estimated Price: ${estimated_price:,.2f}
            Confidence Score: {confidence_score:.2f}
            
            Provide a comprehensive analysis including:
            1. Price justification
            2. Market positioning
            3. Investment potential
            4. Risk factors
            5. Recommendations
            
            Keep the analysis professional and data-driven.
            """
            
            detailed_analysis = await self.llm_service.generate_text(analysis_prompt)
            
            return {
                "summary": detailed_analysis,
                "key_factors": self._extract_key_factors(comparables, market_trends),
                "risk_assessment": self._assess_risks(property_data, market_trends),
                "recommendations": self._generate_recommendations(estimated_price, confidence_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating detailed analysis: {e}")
            return {"summary": "Analysis generation failed", "key_factors": [], "risk_assessment": {}, "recommendations": []}
    
    def _calculate_fallback_price(self, property_data: Dict[str, Any], comparables: List[Dict[str, Any]]) -> float:
        """Calculate fallback price when LLM fails."""
        try:
            if not comparables:
                # Use national average price per sqft
                return property_data.get("square_feet", 1000) * 200  # $200/sqft default
            
            # Use comparable average with adjustments
            prices = []
            for comp in comparables:
                if comp.get("price", 0) > 0 and comp.get("square_feet", 0) > 0:
                    price_per_sqft = comp["price"] / comp["square_feet"]
                    # Adjust for size difference
                    size_diff = (property_data.get("square_feet", 0) - comp["square_feet"]) / comp["square_feet"]
                    adjusted_price = comp["price"] * (1 + size_diff * 0.1)  # 10% adjustment per 100% size difference
                    prices.append(adjusted_price)
            
            return sum(prices) / len(prices) if prices else 0
            
        except Exception as e:
            self.logger.error(f"Error in fallback price calculation: {e}")
            return 0
    
    def _extract_key_factors(self, comparables: List[Dict[str, Any]], market_trends: Dict[str, Any]) -> List[str]:
        """Extract key factors affecting the price estimate."""
        factors = []
        
        if comparables:
            factors.append(f"Based on {len(comparables)} comparable properties")
        
        if market_trends.get("trend_direction") != "unknown":
            factors.append(f"Market trend: {market_trends['trend_direction']}")
        
        if len(comparables) >= 3:
            factors.append("Strong comparable data available")
        elif len(comparables) > 0:
            factors.append("Limited comparable data")
        else:
            factors.append("No comparable properties found")
        
        return factors
    
    def _assess_risks(self, property_data: Dict[str, Any], market_trends: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks associated with the property."""
        risks = {
            "market_risk": "low",
            "data_risk": "low",
            "valuation_risk": "low"
        }
        
        # Market risk assessment
        if market_trends.get("trend_direction") == "declining":
            risks["market_risk"] = "high"
        elif market_trends.get("trend_direction") == "volatile":
            risks["market_risk"] = "medium"
        
        # Data risk assessment
        required_fields = ["bedrooms", "bathrooms", "square_feet"]
        missing_fields = [field for field in required_fields if property_data.get(field) is None]
        if len(missing_fields) > 1:
            risks["data_risk"] = "high"
        elif len(missing_fields) == 1:
            risks["data_risk"] = "medium"
        
        return risks
    
    def _generate_recommendations(self, estimated_price: float, confidence_score: float) -> List[str]:
        """Generate recommendations based on the analysis."""
        recommendations = []
        
        if confidence_score < 0.6:
            recommendations.append("Consider obtaining additional property data for more accurate valuation")
            recommendations.append("Consult with local real estate professionals")
        
        if confidence_score >= 0.8:
            recommendations.append("High confidence in price estimate - suitable for decision making")
        
        recommendations.append("Monitor market conditions for price adjustments")
        recommendations.append("Consider property inspection for hidden issues")
        
        return recommendations
