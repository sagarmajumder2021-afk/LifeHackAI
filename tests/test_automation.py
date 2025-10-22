"""
Tests for the automation scripts.
"""
import pytest
import os
import sys
import json
from datetime import datetime

# Add the automation directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'automation', 'runners'))

from budget_automation import create_budget_snapshot, analyze_budget
from productivity_automation import create_daily_schedule, set_focus_timer

class TestBudgetAutomation:
    """Test cases for budget automation scripts."""
    
    def test_create_budget_snapshot(self):
        """Test creating a budget snapshot."""
        income = 5000.0
        budget = create_budget_snapshot(income, save_to_file=False)
        
        # Check basic structure
        assert "date" in budget
        assert "income" in budget
        assert budget["income"] == income
        assert "expenses" in budget
        assert "savings" in budget
        assert "total_expenses" in budget
        assert "balance" in budget
        assert "analysis" in budget
        
        # Check expense categories
        expenses = budget["expenses"]
        assert "housing" in expenses
        assert "food" in expenses
        assert "transportation" in expenses
        assert "utilities" in expenses
        assert "entertainment" in expenses
        assert "other" in expenses
        
        # Check that percentages add up correctly
        analysis = budget["analysis"]
        total_percent = sum(analysis.values())
        assert abs(total_percent - 100.0) < 0.01  # Allow for small floating point errors
    
    def test_create_budget_snapshot_with_file(self):
        """Test creating a budget snapshot and saving to file."""
        income = 3000.0
        budget = create_budget_snapshot(income, save_to_file=True)
        
        assert "saved_to" in budget
        filename = budget["saved_to"]
        assert os.path.exists(filename)
        
        # Check file contents
        with open(filename, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data["income"] == income
        assert "expenses" in saved_data
        
        # Clean up
        os.remove(filename)
        if os.path.exists("data") and not os.listdir("data"):
            os.rmdir("data")
    
    def test_analyze_budget(self):
        """Test budget analysis."""
        # Create a test budget
        budget = create_budget_snapshot(4000.0, save_to_file=False)
        
        # Analyze it
        analysis = analyze_budget(budget)
        
        assert "summary" in analysis
        assert "date" in analysis
        assert "income" in analysis
        assert "total_expenses" in analysis
        assert "savings" in analysis
        assert "balance" in analysis
        assert "recommendations" in analysis
        
        # Check that recommendations is a list
        assert isinstance(analysis["recommendations"], list)
        assert len(analysis["recommendations"]) > 0

class TestProductivityAutomation:
    """Test cases for productivity automation scripts."""
    
    def test_create_daily_schedule(self):
        """Test creating a daily schedule."""
        start_hour = 9
        end_hour = 17
        schedule = create_daily_schedule(start_hour, end_hour, save_to_file=False)
        
        # Check basic structure
        assert "date" in schedule
        assert "created_at" in schedule
        assert "start_hour" in schedule
        assert schedule["start_hour"] == start_hour
        assert "end_hour" in schedule
        assert schedule["end_hour"] == end_hour
        assert "time_blocks" in schedule
        assert "total_work_hours" in schedule
        assert schedule["total_work_hours"] == end_hour - start_hour
        
        # Check time blocks
        time_blocks = schedule["time_blocks"]
        assert len(time_blocks) == end_hour - start_hour
        
        # Check first time block structure
        first_block = time_blocks[0]
        assert "start_time" in first_block
        assert "end_time" in first_block
        assert "duration_minutes" in first_block
        assert first_block["duration_minutes"] == 60
        assert "task_type" in first_block
        assert "priority" in first_block
        assert "task" in first_block
    
    def test_create_daily_schedule_with_file(self):
        """Test creating a daily schedule and saving to file."""
        schedule = create_daily_schedule(8, 18, save_to_file=True)
        
        assert "saved_to" in schedule
        filename = schedule["saved_to"]
        assert os.path.exists(filename)
        
        # Check file contents
        with open(filename, 'r') as f:
            saved_data = json.load(f)
        
        assert "time_blocks" in saved_data
        assert len(saved_data["time_blocks"]) == 10  # 8 to 18 = 10 hours
        
        # Clean up
        os.remove(filename)
        if os.path.exists("data") and not os.listdir("data"):
            os.rmdir("data")
    
    def test_set_focus_timer(self):
        """Test setting a focus timer."""
        minutes = 25
        task = "Test Task"
        timer = set_focus_timer(minutes, task)
        
        assert "task" in timer
        assert timer["task"] == task
        assert "start_time" in timer
        assert "end_time" in timer
        assert "duration_minutes" in timer
        assert timer["duration_minutes"] == minutes
        assert "status" in timer
        assert timer["status"] == "running"
        
        # Check that start and end times are valid ISO format
        start_time = datetime.fromisoformat(timer["start_time"])
        end_time = datetime.fromisoformat(timer["end_time"])
        
        # Check that the duration is correct
        duration = (end_time - start_time).total_seconds() / 60
        assert abs(duration - minutes) < 1  # Allow for small timing differences

if __name__ == "__main__":
    pytest.main([__file__])