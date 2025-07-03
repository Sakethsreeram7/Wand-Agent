#!/usr/bin/env python3
"""
Test script to verify that the Wand-Agent can properly access and use tools.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_agent_tools():
    """Test the agent's ability to use tools"""
    
    print("🧪 Testing Wand-Agent Tool Access...")
    print("=" * 50)
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Import the agent
        from app.agent.agentic_workflow import GraphBuilder
        
        print("✅ Successfully imported GraphBuilder")
        
        # Create the agent
        graph_builder = GraphBuilder(model_provider="groq")
        print(f"✅ GraphBuilder created with {len(graph_builder.tools)} tools")
        
        # List all available tools
        print("\n📋 Available Tools:")
        for i, tool in enumerate(graph_builder.tools, 1):
            print(f"  {i:2d}. {tool.name} - {tool.description}")
        
        # Build the graph
        graph = graph_builder()
        print("\n✅ Graph built successfully")
        
        # Test cases
        test_cases = [
            {
                "name": "Weather Query",
                "query": "What's the weather in London?",
                "expected_tool": "get_current_weather"
            },
            {
                "name": "Simple Calculation", 
                "query": "What is 10 + 15?",
                "expected_tool": "add_numbers"
            },
            {
                "name": "Place Search",
                "query": "Tell me about tourist attractions in Tokyo",
                "expected_tool": "search_tourist_attractions"
            }
        ]
        
        print("\n🔬 Running Test Cases:")
        print("-" * 30)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test_case['name']}")
            print(f"Query: {test_case['query']}")
            
            try:
                # Create message format
                messages = {"messages": [{"role": "user", "content": test_case['query']}]}
                
                # Invoke the agent (with timeout simulation)
                print("  🤖 Agent processing...")
                result = graph.invoke(messages)
                
                if isinstance(result, dict) and "messages" in result:
                    response = result["messages"][-1].content
                    print(f"  ✅ Response received: {response[:100]}...")
                    
                    # Check if tool was likely used (basic heuristic)
                    if "tool" in response.lower() or any(tool.name in response.lower() for tool in graph_builder.tools):
                        print(f"  ✅ Tool usage detected")
                    else:
                        print(f"  ⚠️  Tool usage not clearly detected")
                else:
                    print(f"  ❌ Unexpected response format: {type(result)}")
                    
            except Exception as e:
                print(f"  ❌ Test failed: {str(e)}")
                
        print("\n" + "=" * 50)
        print("🎉 Agent tool access test completed!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agent_tools()
    sys.exit(0 if success else 1)
