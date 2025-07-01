import math
from typing import Union

class Calculator:
    """Simple calculator for travel expense calculations"""
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract second number from first"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide first number by second"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def percentage(self, value: float, percentage: float) -> float:
        """Calculate percentage of a value"""
        return (value * percentage) / 100
    
    def calculate_total_expense(self, expenses: list) -> float:
        """Calculate total from a list of expenses"""
        return sum(expenses)
    
    def calculate_per_person_cost(self, total_cost: float, num_people: int) -> float:
        """Calculate cost per person"""
        if num_people <= 0:
            raise ValueError("Number of people must be greater than 0")
        return total_cost / num_people
    
    def calculate_daily_budget(self, total_budget: float, num_days: int) -> float:
        """Calculate daily budget from total budget"""
        if num_days <= 0:
            raise ValueError("Number of days must be greater than 0")
        return total_budget / num_days
    
    def compound_calculation(self, principal: float, rate: float, time: float) -> float:
        """Calculate compound interest (useful for budget planning)"""
        return principal * (1 + rate/100) ** time
