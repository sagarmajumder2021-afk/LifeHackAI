"""
Budget automation script for LifeHackAI.

This script creates a simple budget snapshot and provides basic analysis.
"""
import os
import json
import datetime
from typing import Dict, List, Any

def create_budget_snapshot(income: float = 3000.0, save_to_file: bool = True) -> Dict[str, Any]:
    """
    Create a budget snapshot with income, expenses, and savings.
    
    Args:
        income: Monthly income amount
        save_to_file: Whether to save the budget to a file
        
    Returns:
        Dictionary containing the budget snapshot
    """
    # Calculate expense categories as percentages of income
    housing = income * 0.3  # 30% for housing
    food = income * 0.15    # 15% for food
    transport = income * 0.1  # 10% for transportation
    utilities = income * 0.05  # 5% for utilities
    entertainment = income * 0.1  # 10% for entertainment
    savings = income * 0.2  # 20% for savings
    other = income * 0.1  # 10% for other expenses
    
    # Create budget snapshot
    budget = {
        "date": datetime.datetime.now().isoformat(),
        "income": income,
        "expenses": {
            "housing": housing,
            "food": food,
            "transportation": transport,
            "utilities": utilities,
            "entertainment": entertainment,
            "other": other
        },
        "savings": savings,
        "total_expenses": housing + food + transport + utilities + entertainment + other,
        "balance": income - (housing + food + transport + utilities + entertainment + other + savings)
    }
    
    # Add analysis
    budget["analysis"] = {
        "housing_percent": (housing / income) * 100,
        "food_percent": (food / income) * 100,
        "transport_percent": (transport / income) * 100,
        "utilities_percent": (utilities / income) * 100,
        "entertainment_percent": (entertainment / income) * 100,
        "savings_percent": (savings / income) * 100,
        "other_percent": (other / income) * 100
    }
    
    # Save to file if requested
    if save_to_file:
        os.makedirs("data", exist_ok=True)
        filename = f"data/budget_snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(budget, f, indent=2)
        budget["saved_to"] = filename
    
    return budget

def analyze_budget(budget: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a budget snapshot and provide recommendations.
    
    Args:
        budget: Budget snapshot dictionary
        
    Returns:
        Dictionary containing analysis and recommendations
    """
    analysis = {
        "summary": "Budget Analysis",
        "date": datetime.datetime.now().isoformat(),
        "income": budget["income"],
        "total_expenses": budget["total_expenses"],
        "savings": budget["savings"],
        "balance": budget["balance"]
    }
    
    # Generate recommendations
    recommendations = []
    
    # Check housing costs (should be under 30%)
    housing_percent = budget["analysis"]["housing_percent"]
    if housing_percent > 30:
        recommendations.append(f"Housing costs are {housing_percent:.1f}% of income, which is above the recommended 30%. Consider finding ways to reduce housing costs.")
    
    # Check savings (should be at least 20%)
    savings_percent = budget["analysis"]["savings_percent"]
    if savings_percent < 20:
        recommendations.append(f"Savings are only {savings_percent:.1f}% of income, which is below the recommended 20%. Try to increase savings.")
    
    # Check entertainment (should be under 10%)
    entertainment_percent = budget["analysis"]["entertainment_percent"]
    if entertainment_percent > 10:
        recommendations.append(f"Entertainment expenses are {entertainment_percent:.1f}% of income, which is above the recommended 10%. Consider reducing entertainment costs.")
    
    # Add general recommendations
    recommendations.append("Track your expenses daily to stay within budget.")
    recommendations.append("Set up automatic transfers to your savings account on payday.")
    recommendations.append("Review your budget monthly and adjust as needed.")
    
    analysis["recommendations"] = recommendations
    
    return analysis

if __name__ == "__main__":
    # Example usage
    income = float(input("Enter your monthly income (default: 3000): ") or 3000)
    budget = create_budget_snapshot(income)
    analysis = analyze_budget(budget)
    
    print("\n=== Budget Snapshot ===")
    print(f"Income: ${budget['income']:.2f}")
    print(f"Total Expenses: ${budget['total_expenses']:.2f}")
    print(f"Savings: ${budget['savings']:.2f}")
    print(f"Balance: ${budget['balance']:.2f}")
    
    print("\n=== Recommendations ===")
    for i, rec in enumerate(analysis["recommendations"], 1):
        print(f"{i}. {rec}")
    
    if "saved_to" in budget:
        print(f"\nBudget snapshot saved to {budget['saved_to']}")