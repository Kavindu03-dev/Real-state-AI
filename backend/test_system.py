#!/usr/bin/env python3
"""
Test script for the Real Estate AI system.
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_llm_service():
    """Test the LLM service."""
    print("Testing LLM Service...")
    try:
        from app.services.llm_service import LLMService
        
        llm_service = LLMService()
        response = await llm_service.generate_text("Test prompt for real estate analysis")
        print(f"✅ LLM Service: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ LLM Service Error: {e}")
        return False

async def test_data_service():
    """Test the data service."""
    print("Testing Data Service...")
    try:
        from app.services.data_service import DataService
        
        data_service = DataService()
        market_data = await data_service.get_market_data("New York", "NY")
        print(f"✅ Data Service: Market data retrieved for {market_data.get('avg_price', 0)}")
        return True
    except Exception as e:
        print(f"❌ Data Service Error: {e}")
        return False

async def test_nlp_service():
    """Test the NLP service."""
    print("Testing NLP Service...")
    try:
        from app.services.nlp_service import NLPService
        
        nlp_service = NLPService()
        features = await nlp_service.extract_property_features("Beautiful 3 bedroom house with 2 bathrooms")
        print(f"✅ NLP Service: Extracted {len(features)} features")
        return True
    except Exception as e:
        print(f"❌ NLP Service Error: {e}")
        return False

async def test_agents():
    """Test the agents."""
    print("Testing Agents...")
    try:
        from app.agents.price_estimator import PriceEstimatorAgent
        from app.agents.location_analyzer import LocationAnalyzerAgent
        from app.agents.deal_evaluator import DealEvaluatorAgent
        
        # Test price estimator
        price_agent = PriceEstimatorAgent()
        await price_agent.startup()
        
        # Test location analyzer
        location_agent = LocationAnalyzerAgent()
        await location_agent.startup()
        
        # Test deal evaluator
        deal_agent = DealEvaluatorAgent()
        await deal_agent.startup()
        
        print("✅ All agents initialized successfully")
        
        # Cleanup
        await price_agent.shutdown()
        await location_agent.shutdown()
        await deal_agent.shutdown()
        
        return True
    except Exception as e:
        print(f"❌ Agents Error: {e}")
        return False

async def test_orchestrator():
    """Test the orchestrator."""
    print("Testing Orchestrator...")
    try:
        from app.agents.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        await orchestrator.startup()
        
        # Test agent status
        status = await orchestrator.get_agent_status()
        print(f"✅ Orchestrator: {len(status)} agents available")
        
        await orchestrator.shutdown()
        return True
    except Exception as e:
        print(f"❌ Orchestrator Error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 Testing Real Estate AI System Components\n")
    
    tests = [
        test_llm_service(),
        test_data_service(),
        test_nlp_service(),
        test_agents(),
        test_orchestrator()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    print("\n📊 Test Results:")
    print("=" * 50)
    
    test_names = [
        "LLM Service",
        "Data Service", 
        "NLP Service",
        "Agents",
        "Orchestrator"
    ]
    
    passed = 0
    for i, result in enumerate(results):
        if result is True:
            print(f"✅ {test_names[i]}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_names[i]}: FAILED")
    
    print("=" * 50)
    print(f"🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! System is ready to run.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
