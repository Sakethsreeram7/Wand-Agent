from ..utils.currency_converter import CurrencyConverter
from langchain.tools import tool
from typing import List

class CurrencyConverterTool:
    def __init__(self):
        self.currency_converter = CurrencyConverter()
        self.currency_converter_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup all currency converter tools"""
        
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
            """Convert amount from one currency to another. Use 3-letter currency codes like USD, EUR, GBP, etc."""
            try:
                converted_amount = self.currency_converter.convert_currency(amount, from_currency, to_currency)
                if converted_amount > 0:
                    return f"{amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()}"
                else:
                    return f"Unable to convert {from_currency} to {to_currency}. Please check currency codes."
            except Exception as e:
                return f"Error converting currency: {str(e)}"
        
        @tool
        def get_exchange_rate(from_currency: str, to_currency: str) -> str:
            """Get current exchange rate between two currencies"""
            try:
                rate = self.currency_converter.get_exchange_rate(from_currency, to_currency)
                if rate > 0:
                    return f"1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"
                else:
                    return f"Unable to get exchange rate for {from_currency} to {to_currency}"
            except Exception as e:
                return f"Error getting exchange rate: {str(e)}"
        
        @tool
        def get_supported_currencies() -> str:
            """Get list of supported currencies with their full names"""
            try:
                currencies = self.currency_converter.get_supported_currencies()
                result = "Supported currencies:\n"
                for code, name in currencies.items():
                    result += f"- {code}: {name}\n"
                return result
            except Exception as e:
                return f"Error getting supported currencies: {str(e)}"
        
        @tool
        def convert_multiple_currencies(amount: float, from_currency: str, to_currencies: str) -> str:
            """Convert amount to multiple currencies. Provide to_currencies as comma-separated string (e.g., 'USD,EUR,GBP')"""
            try:
                currency_list = [currency.strip() for currency in to_currencies.split(',')]
                rates = self.currency_converter.get_multiple_rates(from_currency, currency_list)
                
                result = f"Converting {amount} {from_currency.upper()}:\n"
                for currency, rate in rates.items():
                    if rate > 0:
                        converted_amount = amount * rate
                        result += f"- {currency}: {converted_amount:.2f}\n"
                    else:
                        result += f"- {currency}: Unable to convert\n"
                
                return result
            except Exception as e:
                return f"Error converting to multiple currencies: {str(e)}"
        
        return [
            convert_currency,
            get_exchange_rate,
            get_supported_currencies,
            convert_multiple_currencies
        ]
