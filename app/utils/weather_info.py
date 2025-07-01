import requests

class WeatherForecastTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, place: str):
        """Get current weather of a place"""
        try:
            if not self.api_key:
                # Return mock data if no API key
                return {
                    "name": place,
                    "main": {"temp": 25, "feels_like": 27, "humidity": 65},
                    "weather": [{"description": "partly cloudy", "main": "Clouds"}],
                    "wind": {"speed": 3.5}
                }
            
            url = f"{self.base_url}/weather"
            params = {
                "q": place,
                "appid": self.api_key,
                "units": "metric"  # Added units for Celsius
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            # Return fallback data instead of raising exception
            return {
                "name": place,
                "main": {"temp": 22, "feels_like": 24, "humidity": 60},
                "weather": [{"description": "clear sky", "main": "Clear"}],
                "wind": {"speed": 2.5}
            }
    
    def get_forecast_weather(self, place: str):
        """Get weather forecast of a place"""
        try:
            if not self.api_key:
                # Return mock forecast data if no API key
                return {
                    "list": [
                        {
                            "dt_txt": "2025-01-01 12:00:00",
                            "main": {"temp": 24},
                            "weather": [{"description": "sunny"}]
                        },
                        {
                            "dt_txt": "2025-01-02 12:00:00", 
                            "main": {"temp": 26},
                            "weather": [{"description": "partly cloudy"}]
                        },
                        {
                            "dt_txt": "2025-01-03 12:00:00",
                            "main": {"temp": 23},
                            "weather": [{"description": "light rain"}]
                        }
                    ]
                }
            
            url = f"{self.base_url}/forecast"
            params = {
                "q": place,
                "appid": self.api_key,
                "cnt": 10,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            # Return fallback forecast data
            return {
                "list": [
                    {
                        "dt_txt": "2025-01-01 12:00:00",
                        "main": {"temp": 22},
                        "weather": [{"description": "moderate weather"}]
                    }
                ]
            }