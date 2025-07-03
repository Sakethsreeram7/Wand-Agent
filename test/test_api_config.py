#!/usr/bin/env python3
"""
Test script to check API key configuration and direct weather service
"""

import sys
import os
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.weather_info import WeatherForecastTool

def test_api_key_config():
    """Test API key configuration"""
    print("🔑 Testing API Key Configuration")
    print("=" * 50)
    
    load_dotenv()
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
    
    if api_key:
        print(f"✅ OpenWeatherMap API Key found: {api_key[:8]}...")
        print(f"📡 Using real OpenWeatherMap API")
    else:
        print("⚠️  No OpenWeatherMap API Key found in environment")
        print("🔄 Using mock data fallback")
    
    print("\n" + "=" * 50)
    print("🧪 Testing Direct Weather Service")
    print("=" * 50)
    
    weather_service = WeatherForecastTool(api_key)
    
    # Test current weather
    print("Testing current weather for Paris...")
    current_weather = weather_service.get_current_weather("Paris")
    print(f"Response: {current_weather}")
    
    print("\nTesting forecast for Paris...")
    forecast = weather_service.get_forecast_weather("Paris")
    print(f"Forecast items: {len(forecast.get('list', []))}")

if __name__ == "__main__":
    test_api_key_config()
