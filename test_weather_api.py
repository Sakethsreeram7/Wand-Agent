#!/usr/bin/env python3
"""
Test script for the Weather API functionality
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.tools.weather_info_tool import WeatherInfoTool

def test_weather_api():
    """Test the weather API functionality"""
    print("🌤️  Testing Weather API Functionality")
    print("=" * 50)
    
    # Initialize the weather tool
    weather_tool = WeatherInfoTool()
    tools = weather_tool.weather_tool_list
    
    print(f"✅ Weather tool initialized successfully!")
    print(f"📊 Available tools: {len(tools)}")
    
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    print("\n" + "=" * 50)
    print("🧪 Testing Current Weather Tool")
    print("=" * 50)
    
    # Test current weather
    current_weather_tool = tools[0]  # get_current_weather
    test_cities = ["New York", "Bangalore", "Tokyo", "Paris"]
    
    for city in test_cities:
        try:
            result = current_weather_tool.invoke(city)
            print(f"🌍 {city}: {result}")
        except Exception as e:
            print(f"❌ Error testing {city}: {e}")
    
    print("\n" + "=" * 50)
    print("🔮 Testing Weather Forecast Tool")
    print("=" * 50)
    
    # Test weather forecast
    forecast_tool = tools[1]  # get_weather_forecast
    
    for city in test_cities[:2]:  # Test with first 2 cities
        try:
            result = forecast_tool.invoke(city)
            print(f"📅 Forecast for {city}:")
            print(result)
            print("-" * 30)
        except Exception as e:
            print(f"❌ Error testing forecast for {city}: {e}")

if __name__ == "__main__":
    test_weather_api()
