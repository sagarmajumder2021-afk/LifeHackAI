"""
AI plan generation module for LifeHackAI.
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import random

# In a production app, this would use OpenAI or another LLM
# For demo purposes, we'll use predefined plans

# Sample plans for different problem categories
SAMPLE_PLANS = {
    "shopping": {
        "summary": "Optimize your weekly grocery shopping to save time and money",
        "steps": [
            {"step_id": 1, "title": "Create a meal plan", "details": "Plan your meals for the week to know exactly what you need", "due_offset": "0h"},
            {"step_id": 2, "title": "Take inventory", "details": "Check what you already have to avoid buying duplicates", "due_offset": "1h"},
            {"step_id": 3, "title": "Make a shopping list", "details": "Create a detailed list organized by store sections", "due_offset": "2h"},
            {"step_id": 4, "title": "Compare prices online", "details": "Check weekly ads and apps for deals", "due_offset": "1d"},
            {"step_id": 5, "title": "Shop during off-peak hours", "details": "Go early morning or late evening to avoid crowds", "due_offset": "2d"},
            {"step_id": 6, "title": "Batch cook and freeze", "details": "Prepare meals in bulk to save time later", "due_offset": "3d"}
        ]
    },
    "productivity": {
        "summary": "Establish an effective morning routine for better daily productivity",
        "steps": [
            {"step_id": 1, "title": "Plan the night before", "details": "Set out your priorities for the next day before bed", "due_offset": "0h"},
            {"step_id": 2, "title": "Wake up consistently", "details": "Set a regular wake-up time, even on weekends", "due_offset": "1d"},
            {"step_id": 3, "title": "Hydrate first", "details": "Drink a glass of water before anything else", "due_offset": "1d"},
            {"step_id": 4, "title": "No screens for 30 minutes", "details": "Avoid checking email or social media right away", "due_offset": "1d"},
            {"step_id": 5, "title": "Exercise briefly", "details": "Do 5-10 minutes of stretching or light movement", "due_offset": "1d"},
            {"step_id": 6, "title": "Review your day's plan", "details": "Check your calendar and top priorities", "due_offset": "1d"}
        ]
    },
    "finance": {
        "summary": "Create and maintain a personal monthly budget",
        "steps": [
            {"step_id": 1, "title": "Track current spending", "details": "Record all expenses for two weeks to establish a baseline", "due_offset": "0h"},
            {"step_id": 2, "title": "Categorize expenses", "details": "Group spending into categories (housing, food, transport, etc.)", "due_offset": "14d"},
            {"step_id": 3, "title": "Set category limits", "details": "Establish reasonable spending limits for each category", "due_offset": "15d"},
            {"step_id": 4, "title": "Create a budget document", "details": "Use a spreadsheet or app to formalize your budget", "due_offset": "16d"},
            {"step_id": 5, "title": "Set up tracking system", "details": "Choose a method to track expenses against budget", "due_offset": "17d"},
            {"step_id": 6, "title": "Schedule weekly reviews", "details": "Set aside 15 minutes weekly to review and adjust", "due_offset": "18d"}
        ]
    },
    "general": {
        "summary": "Solve your daily life problem with a structured approach",
        "steps": [
            {"step_id": 1, "title": "Define the problem clearly", "details": "Write down exactly what you're trying to solve", "due_offset": "0h"},
            {"step_id": 2, "title": "Break it into smaller parts", "details": "Divide the problem into manageable components", "due_offset": "1h"},
            {"step_id": 3, "title": "Research solutions", "details": "Look for how others have solved similar problems", "due_offset": "1d"},
            {"step_id": 4, "title": "Create an action plan", "details": "List specific steps with deadlines", "due_offset": "2d"},
            {"step_id": 5, "title": "Execute first step", "details": "Complete the first action item", "due_offset": "3d"},
            {"step_id": 6, "title": "Review and adjust", "details": "Evaluate progress and modify plan as needed", "due_offset": "7d"}
        ]
    }
}

def generate_plan(problem_id: int) -> Dict[str, Any]:
    """
    Generate an AI plan for a given problem.
    
    In a production app, this would call OpenAI API or another LLM.
    For demo purposes, we're using predefined plans.
    
    Args:
        problem_id: ID of the problem to generate a plan for
        
    Returns:
        Dictionary containing the plan details
    """
    # In a real app, we would fetch the problem details from the database
    # and use them to generate a customized plan
    
    # For demo, we'll map problem IDs to categories
    problem_categories = {
        1: "shopping",
        2: "productivity",
        3: "finance",
        4: "general"
    }
    
    category = problem_categories.get(problem_id, "general")
    plan_template = SAMPLE_PLANS.get(category, SAMPLE_PLANS["general"])
    
    # Create the plan response
    plan = {
        "plan_id": 1,  # In a real app, this would be generated by the database
        "problem_id": problem_id,
        "generated_at": datetime.now().isoformat(),
        "summary": plan_template["summary"],
        "steps": plan_template["steps"]
    }
    
    return plan

def parse_due_offset(offset: str) -> int:
    """
    Parse a due offset string (e.g., '2h', '1d') into minutes.
    
    Args:
        offset: String representing time offset
        
    Returns:
        Number of minutes
    """
    unit = offset[-1]
    value = int(offset[:-1])
    
    if unit == 'h':
        return value * 60  # hours to minutes
    elif unit == 'd':
        return value * 24 * 60  # days to minutes
    elif unit == 'w':
        return value * 7 * 24 * 60  # weeks to minutes
    else:
        return value  # assume minutes