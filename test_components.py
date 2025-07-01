#!/usr/bin/env python3
"""
Test script to verify the AI Trip Planner components work correctly
"""

import os
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    weather_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    print("🔧 Environment Check:")
    print(f"  GROQ_API_KEY: {'✓ Set' if groq_key else '✗ Not set'}")
    print(f"  OPENWEATHERMAP_API_KEY: {'✓ Set' if weather_key else '✗ Not set (will use mock data)'}")
    
    return groq_key is not None

def test_tools():
    """Test individual tools"""
    print("\n🛠️  Tool Tests:")
    
    # Test Calculator
    try:
        from app.tools.expense_calculator_tool import CalculatorTool
        calc_tool = CalculatorTool()
        print(f"  Calculator Tool: ✓ {len(calc_tool.calculator_tool_list)} tools loaded")
    except Exception as e:
        print(f"  Calculator Tool: ✗ {e}")
    
    # Test Currency Converter
    try:
        from app.tools.currency_conversion_tool import CurrencyConverterTool
        currency_tool = CurrencyConverterTool()
        print(f"  Currency Tool: ✓ {len(currency_tool.currency_converter_tool_list)} tools loaded")
    except Exception as e:
        print(f"  Currency Tool: ✗ {e}")
    
    # Test Weather Tool
    try:
        from app.tools.weather_info_tool import WeatherInfoTool
        weather_tool = WeatherInfoTool()
        print(f"  Weather Tool: ✓ {len(weather_tool.weather_tool_list)} tools loaded")
    except Exception as e:
        print(f"  Weather Tool: ✗ {e}")
    
    # Test Place Search Tool
    try:
        from app.tools.place_search_tool import PlaceSearchTool
        place_tool = PlaceSearchTool()
        print(f"  Place Search Tool: ✓ {len(place_tool.place_search_tool_list)} tools loaded")
    except Exception as e:
        print(f"  Place Search Tool: ✗ {e}")

def test_agent():
    """Test agent initialization"""
    print("\n🤖 Agent Test:")
    
    try:
        from app.agent.agentic_workflow import GraphBuilder
        graph_builder = GraphBuilder(model_provider="groq")
        agent = graph_builder()
        print("  Agent Initialization: ✓ Success")
        print(f"  Agent Type: {type(agent)}")
        return True
    except Exception as e:
        print(f"  Agent Initialization: ✗ {e}")
        return False

def test_simple_query():
    """Test a simple query if agent works"""
    print("\n🧪 Simple Query Test:")
    
    try:
        from app.agent.agentic_workflow import GraphBuilder
        
        graph_builder = GraphBuilder(model_provider="groq")
        agent = graph_builder()
        
        # Simple test query
        test_messages = {"messages": [{"role": "user", "content": "What's 100 + 200?"}]}
        
        print("  Running simple calculation query...")
        result = agent.invoke(test_messages)
        
        if result and "messages" in result:
            response = result["messages"][-1].content
            print(f"  Query Result: ✓ {response[:100]}...")
        else:
            print(f"  Query Result: ✓ {str(result)[:100]}...")
            
        return True
        
    except Exception as e:
        print(f"  Simple Query: ✗ {e}")
        return False

def main():
    """Run all tests"""
    print("🌍 AI Trip Planner - Component Test\n")
    
    # Test environment
    env_ok = test_environment()
    
    # Test tools
    test_tools()
    
    # Test agent
    agent_ok = test_agent()
    
    # Test simple query if everything is working
    if env_ok and agent_ok:
        test_simple_query()
    
    print("\n" + "="*50)
    print("🎉 Component test completed!")
    print("If all tests show ✓, your AI Trip Planner is ready to use!")
    print("\nNext steps:")
    print("1. Start FastAPI: python run.py api")
    print("2. Start Streamlit: python run.py web")

if __name__ == "__main__":
    main()
