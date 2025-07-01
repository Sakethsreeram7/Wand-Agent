import requests
from typing import Dict, List, Optional
import time

class PlaceInfoSearch:
    """Place information search using free OpenStreetMap Nominatim API"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {
            'User-Agent': 'AI_Trip_Planner/1.0 (educational_project)'
        }
        
    def search_place(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for places using query"""
        try:
            url = f"{self.base_url}/search"
            params = {
                'q': query,
                'format': 'json',
                'limit': limit,
                'addressdetails': 1,
                'extratags': 1
            }
            
            response = requests.get(url, params=params, headers=self.headers)
            time.sleep(1)  # Be respectful to free API
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"Error searching place: {e}")
            return []
    
    def get_place_details(self, place_name: str) -> Dict:
        """Get detailed information about a place"""
        try:
            places = self.search_place(place_name, limit=1)
            if places:
                place = places[0]
                return {
                    'name': place.get('display_name', 'Unknown'),
                    'latitude': place.get('lat', ''),
                    'longitude': place.get('lon', ''),
                    'type': place.get('type', 'Unknown'),
                    'category': place.get('class', 'Unknown'),
                    'importance': place.get('importance', 0),
                    'address': place.get('address', {}),
                    'country': place.get('address', {}).get('country', 'Unknown'),
                    'state': place.get('address', {}).get('state', 'Unknown'),
                    'city': place.get('address', {}).get('city', 'Unknown')
                }
            else:
                return {}
                
        except Exception as e:
            print(f"Error getting place details: {e}")
            return {}
    
    def search_nearby_attractions(self, place_name: str) -> List[Dict]:
        """Search for tourist attractions near a place"""
        try:
            # First get the place coordinates
            place_details = self.get_place_details(place_name)
            if not place_details:
                return []
            
            lat = place_details.get('latitude')
            lon = place_details.get('longitude')
            
            if not lat or not lon:
                return []
            
            # Search for tourist attractions nearby
            url = f"{self.base_url}/search"
            params = {
                'q': f'tourist attraction near {place_name}',
                'format': 'json',
                'limit': 10,
                'addressdetails': 1
            }
            
            response = requests.get(url, params=params, headers=self.headers)
            time.sleep(1)  # Be respectful to free API
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"Error searching nearby attractions: {e}")
            return []
    
    def search_restaurants(self, place_name: str) -> List[Dict]:
        """Search for restaurants in a place"""
        try:
            url = f"{self.base_url}/search"
            params = {
                'q': f'restaurant {place_name}',
                'format': 'json',
                'limit': 10,
                'addressdetails': 1
            }
            
            response = requests.get(url, params=params, headers=self.headers)
            time.sleep(1)  # Be respectful to free API
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"Error searching restaurants: {e}")
            return []
    
    def search_hotels(self, place_name: str) -> List[Dict]:
        """Search for hotels in a place"""
        try:
            url = f"{self.base_url}/search"
            params = {
                'q': f'hotel {place_name}',
                'format': 'json',
                'limit': 10,
                'addressdetails': 1
            }
            
            response = requests.get(url, params=params, headers=self.headers)
            time.sleep(1)  # Be respectful to free API
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"Error searching hotels: {e}")
            return []
    
    def get_travel_info(self, place_name: str) -> Dict:
        """Get comprehensive travel information about a place"""
        try:
            place_details = self.get_place_details(place_name)
            attractions = self.search_nearby_attractions(place_name)
            restaurants = self.search_restaurants(place_name)
            hotels = self.search_hotels(place_name)
            
            return {
                'place_details': place_details,
                'attractions': attractions[:5],  # Top 5 attractions
                'restaurants': restaurants[:5],  # Top 5 restaurants
                'hotels': hotels[:5]  # Top 5 hotels
            }
            
        except Exception as e:
            print(f"Error getting travel info: {e}")
            return {}
