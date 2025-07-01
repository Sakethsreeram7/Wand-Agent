from ..utils.place_info_search import PlaceInfoSearch
from langchain.tools import tool
from typing import List

class PlaceSearchTool:
    def __init__(self):
        self.place_search = PlaceInfoSearch()
        self.place_search_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup all place search tools"""
        
        @tool
        def search_place_info(place_name: str) -> str:
            """Get basic information about a place including location, type, and address"""
            try:
                place_details = self.place_search.get_place_details(place_name)
                if place_details:
                    return f"""Place Information for {place_name}:
- Full Name: {place_details.get('name', 'Unknown')}
- Type: {place_details.get('type', 'Unknown')}
- Category: {place_details.get('category', 'Unknown')}
- Country: {place_details.get('country', 'Unknown')}
- State/Region: {place_details.get('state', 'Unknown')}
- City: {place_details.get('city', 'Unknown')}
- Coordinates: {place_details.get('latitude', '')}, {place_details.get('longitude', '')}
- Importance Score: {place_details.get('importance', 0)}"""
                else:
                    return f"No information found for {place_name}"
            except Exception as e:
                return f"Error searching place info: {str(e)}"
        
        @tool
        def search_tourist_attractions(place_name: str) -> str:
            """Find tourist attractions and points of interest near a place"""
            try:
                attractions = self.place_search.search_nearby_attractions(place_name)
                if attractions:
                    result = f"Tourist Attractions near {place_name}:\n\n"
                    for i, attraction in enumerate(attractions[:5], 1):
                        name = attraction.get('display_name', 'Unknown')
                        attraction_type = attraction.get('type', 'Unknown')
                        result += f"{i}. {name}\n   Type: {attraction_type}\n\n"
                    return result
                else:
                    return f"No tourist attractions found near {place_name}"
            except Exception as e:
                return f"Error searching attractions: {str(e)}"
        
        @tool
        def search_restaurants(place_name: str) -> str:
            """Find restaurants and dining options in a place"""
            try:
                restaurants = self.place_search.search_restaurants(place_name)
                if restaurants:
                    result = f"Restaurants in {place_name}:\n\n"
                    for i, restaurant in enumerate(restaurants[:5], 1):
                        name = restaurant.get('display_name', 'Unknown')
                        address = restaurant.get('address', {})
                        street = address.get('road', address.get('street', ''))
                        result += f"{i}. {name}\n"
                        if street:
                            result += f"   Address: {street}\n"
                        result += "\n"
                    return result
                else:
                    return f"No restaurants found in {place_name}"
            except Exception as e:
                return f"Error searching restaurants: {str(e)}"
        
        @tool
        def search_hotels(place_name: str) -> str:
            """Find hotels and accommodation options in a place"""
            try:
                hotels = self.place_search.search_hotels(place_name)
                if hotels:
                    result = f"Hotels in {place_name}:\n\n"
                    for i, hotel in enumerate(hotels[:5], 1):
                        name = hotel.get('display_name', 'Unknown')
                        address = hotel.get('address', {})
                        street = address.get('road', address.get('street', ''))
                        result += f"{i}. {name}\n"
                        if street:
                            result += f"   Address: {street}\n"
                        result += "\n"
                    return result
                else:
                    return f"No hotels found in {place_name}"
            except Exception as e:
                return f"Error searching hotels: {str(e)}"
        
        @tool
        def get_comprehensive_travel_info(place_name: str) -> str:
            """Get comprehensive travel information including attractions, restaurants, and hotels for a place"""
            try:
                travel_info = self.place_search.get_travel_info(place_name)
                
                if not travel_info:
                    return f"No travel information found for {place_name}"
                
                result = f"# Comprehensive Travel Information for {place_name}\n\n"
                
                # Place details
                place_details = travel_info.get('place_details', {})
                if place_details:
                    result += f"## Basic Information\n"
                    result += f"- Location: {place_details.get('country', 'Unknown')}, {place_details.get('state', 'Unknown')}\n"
                    result += f"- Type: {place_details.get('type', 'Unknown')}\n"
                    result += f"- Coordinates: {place_details.get('latitude', '')}, {place_details.get('longitude', '')}\n\n"
                
                # Attractions
                attractions = travel_info.get('attractions', [])
                if attractions:
                    result += f"## Top Attractions\n"
                    for i, attraction in enumerate(attractions, 1):
                        name = attraction.get('display_name', 'Unknown')
                        result += f"{i}. {name}\n"
                    result += "\n"
                
                # Restaurants
                restaurants = travel_info.get('restaurants', [])
                if restaurants:
                    result += f"## Restaurants\n"
                    for i, restaurant in enumerate(restaurants, 1):
                        name = restaurant.get('display_name', 'Unknown')
                        result += f"{i}. {name}\n"
                    result += "\n"
                
                # Hotels
                hotels = travel_info.get('hotels', [])
                if hotels:
                    result += f"## Hotels\n"
                    for i, hotel in enumerate(hotels, 1):
                        name = hotel.get('display_name', 'Unknown')
                        result += f"{i}. {name}\n"
                    result += "\n"
                
                return result
                
            except Exception as e:
                return f"Error getting comprehensive travel info: {str(e)}"
        
        return [
            search_place_info,
            search_tourist_attractions,
            search_restaurants,
            search_hotels,
            get_comprehensive_travel_info
        ]
