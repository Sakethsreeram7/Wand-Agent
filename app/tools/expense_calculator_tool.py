from ..utils.calculator import Calculator
from langchain.tools import tool
from typing import List

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup all calculator tools"""
        
        @tool
        def add_numbers(a: float, b: float) -> str:
            """Add two numbers together"""
            try:
                result = self.calculator.add(a, b)
                return f"Result: {a} + {b} = {result}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def multiply_numbers(a: float, b: float) -> str:
            """Multiply two numbers"""
            try:
                result = self.calculator.multiply(a, b)
                return f"Result: {a} × {b} = {result}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def calculate_percentage(value: float, percentage: float) -> str:
            """Calculate percentage of a value"""
            try:
                result = self.calculator.percentage(value, percentage)
                return f"Result: {percentage}% of {value} = {result}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def calculate_total_expenses(expenses: str) -> str:
            """Calculate total expenses from a comma-separated string of numbers"""
            try:
                expense_list = [float(x.strip()) for x in expenses.split(',')]
                total = self.calculator.calculate_total_expense(expense_list)
                return f"Total expenses: {total}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def calculate_per_person_cost(total_cost: float, num_people: int) -> str:
            """Calculate cost per person from total cost and number of people"""
            try:
                cost_per_person = self.calculator.calculate_per_person_cost(total_cost, num_people)
                return f"Cost per person: {cost_per_person} (Total: {total_cost}, People: {num_people})"
            except Exception as e:
                return f"Error: {str(e)}"
        
        @tool
        def calculate_daily_budget(total_budget: float, num_days: int) -> str:
            """Calculate daily budget from total budget and number of days"""
            try:
                daily_budget = self.calculator.calculate_daily_budget(total_budget, num_days)
                return f"Daily budget: {daily_budget} (Total budget: {total_budget}, Days: {num_days})"
            except Exception as e:
                return f"Error: {str(e)}"
        
        return [
            add_numbers, 
            multiply_numbers, 
            calculate_percentage, 
            calculate_total_expenses, 
            calculate_per_person_cost, 
            calculate_daily_budget
        ]
