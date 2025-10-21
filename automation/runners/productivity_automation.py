"""
Productivity automation script for LifeHackAI.

This script helps with time management and productivity tasks.
"""
import os
import json
import datetime
import webbrowser
from typing import Dict, List, Any, Optional

def create_daily_schedule(start_hour: int = 8, end_hour: int = 18, 
                          save_to_file: bool = True) -> Dict[str, Any]:
    """
    Create a daily schedule with time blocks and tasks.
    
    Args:
        start_hour: Hour to start the schedule (24-hour format)
        end_hour: Hour to end the schedule (24-hour format)
        save_to_file: Whether to save the schedule to a file
        
    Returns:
        Dictionary containing the daily schedule
    """
    # Create time blocks
    time_blocks = []
    current_date = datetime.datetime.now().date()
    
    for hour in range(start_hour, end_hour):
        # Morning focus block
        if 8 <= hour < 12:
            task_type = "Deep Work"
            priority = "High"
        # Lunch break
        elif hour == 12:
            task_type = "Break"
            priority = "Medium"
        # Afternoon collaboration
        elif 13 <= hour < 16:
            task_type = "Collaboration"
            priority = "Medium"
        # End of day wrap-up
        else:
            task_type = "Wrap-up"
            priority = "Low"
        
        start_time = datetime.datetime.combine(current_date, datetime.time(hour, 0))
        end_time = datetime.datetime.combine(current_date, datetime.time(hour + 1, 0))
        
        time_blocks.append({
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_minutes": 60,
            "task_type": task_type,
            "priority": priority,
            "task": f"Scheduled {task_type} time"
        })
    
    # Create schedule
    schedule = {
        "date": current_date.isoformat(),
        "created_at": datetime.datetime.now().isoformat(),
        "start_hour": start_hour,
        "end_hour": end_hour,
        "time_blocks": time_blocks,
        "total_work_hours": end_hour - start_hour,
        "deep_work_blocks": sum(1 for block in time_blocks if block["task_type"] == "Deep Work"),
        "break_blocks": sum(1 for block in time_blocks if block["task_type"] == "Break")
    }
    
    # Save to file if requested
    if save_to_file:
        os.makedirs("data", exist_ok=True)
        filename = f"data/daily_schedule_{current_date.strftime('%Y%m%d')}.json"
        with open(filename, "w") as f:
            json.dump(schedule, f, indent=2)
        schedule["saved_to"] = filename
    
    return schedule

def set_focus_timer(minutes: int = 25, task: str = "Focus Work") -> Dict[str, Any]:
    """
    Set a focus timer (Pomodoro technique).
    
    Args:
        minutes: Number of minutes for the focus session
        task: Description of the task
        
    Returns:
        Dictionary containing the timer information
    """
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(minutes=minutes)
    
    timer = {
        "task": task,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_minutes": minutes,
        "status": "running"
    }
    
    # In a real app, this would start an actual timer
    # For demo purposes, we just return the information
    
    print(f"Focus timer started for {minutes} minutes: {task}")
    print(f"Start: {start_time.strftime('%H:%M:%S')}")
    print(f"End: {end_time.strftime('%H:%M:%S')}")
    
    return timer

def open_productivity_tools(tool: str = "all") -> Dict[str, Any]:
    """
    Open productivity tools in the browser.
    
    Args:
        tool: Which tool to open (all, trello, notion, calendar)
        
    Returns:
        Dictionary containing the opened tools
    """
    tools = {
        "trello": "https://trello.com",
        "notion": "https://notion.so",
        "calendar": "https://calendar.google.com",
        "todoist": "https://todoist.com"
    }
    
    opened = []
    
    if tool.lower() == "all":
        for name, url in tools.items():
            try:
                webbrowser.open(url)
                opened.append(name)
            except Exception as e:
                print(f"Error opening {name}: {e}")
    elif tool.lower() in tools:
        try:
            webbrowser.open(tools[tool.lower()])
            opened.append(tool.lower())
        except Exception as e:
            print(f"Error opening {tool}: {e}")
    else:
        print(f"Unknown tool: {tool}")
    
    return {
        "requested_tool": tool,
        "opened_tools": opened,
        "timestamp": datetime.datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Example usage
    print("=== Productivity Automation ===")
    print("1. Create daily schedule")
    print("2. Set focus timer")
    print("3. Open productivity tools")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        start_hour = int(input("Enter start hour (0-23, default: 8): ") or 8)
        end_hour = int(input("Enter end hour (0-23, default: 18): ") or 18)
        schedule = create_daily_schedule(start_hour, end_hour)
        print(f"Schedule created with {schedule['total_work_hours']} work hours")
        if "saved_to" in schedule:
            print(f"Schedule saved to {schedule['saved_to']}")
    
    elif choice == "2":
        minutes = int(input("Enter focus time in minutes (default: 25): ") or 25)
        task = input("Enter task description: ") or "Focus Work"
        timer = set_focus_timer(minutes, task)
    
    elif choice == "3":
        tool = input("Enter tool to open (all, trello, notion, calendar, todoist): ") or "all"
        result = open_productivity_tools(tool)
        print(f"Opened tools: {', '.join(result['opened_tools'])}")
    
    else:
        print("Invalid choice")