import requests
from typing import Dict, Optional
import json

class CurrencyConverter:
    """Currency converter using free exchangerate-api.com API"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Using free tier which doesn't require API key
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        self.api_key = api_key
        
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate between two currencies"""
        try:
            url = f"{self.base_url}/{from_currency.upper()}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                return rates.get(to_currency.upper(), 0.0)
            else:
                return 0.0
                
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return 0.0
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount from one currency to another"""
        try:
            if from_currency.upper() == to_currency.upper():
                return amount
                
            rate = self.get_exchange_rate(from_currency, to_currency)
            if rate > 0:
                return amount * rate
            else:
                return 0.0
                
        except Exception as e:
            print(f"Error converting currency: {e}")
            return 0.0
    
    def get_supported_currencies(self) -> Dict[str, str]:
        """Get list of commonly supported currencies"""
        # Common currencies - this is a static list for free tier
        return {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "KRW": "South Korean Won",
            "SGD": "Singapore Dollar",
            "HKD": "Hong Kong Dollar",
            "NZD": "New Zealand Dollar",
            "SEK": "Swedish Krona",
            "NOK": "Norwegian Krone",
            "MXN": "Mexican Peso",
            "BRL": "Brazilian Real",
            "RUB": "Russian Ruble",
            "ZAR": "South African Rand",
            "THB": "Thai Baht"
        }
    
    def get_multiple_rates(self, from_currency: str, to_currencies: list) -> Dict[str, float]:
        """Get exchange rates for multiple target currencies"""
        rates = {}
        try:
            url = f"{self.base_url}/{from_currency.upper()}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                api_rates = data.get('rates', {})
                
                for currency in to_currencies:
                    rates[currency.upper()] = api_rates.get(currency.upper(), 0.0)
                    
        except Exception as e:
            print(f"Error fetching multiple rates: {e}")
            
        return rates
