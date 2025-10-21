"""
Task management module for LifeHackAI.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime

class TaskManager:
    """
    Manages tasks created from plans.
    
    In a production app, this would use a database.
    For demo purposes, we're using in-memory storage.
    """
    
    def __init__(self):
        """Initialize the task manager with empty task list."""
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, plan_id: int, title: str, due_at: str) -> int:
        """
        Add a new task.
        
        Args:
            plan_id: ID of the plan this task belongs to
            title: Title of the task
            due_at: Due date and time (ISO format)
            
        Returns:
            ID of the newly created task
        """
        task = {
            "id": self.next_id,
            "plan_id": plan_id,
            "title": title,
            "due_at": due_at,
            "status": "pending"
        }
        self.tasks.append(task)
        self.next_id += 1
        return task["id"]
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task dictionary or None if not found
        """
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self.tasks
    
    def get_tasks_by_plan(self, plan_id: int) -> List[Dict[str, Any]]:
        """
        Get all tasks for a specific plan.
        
        Args:
            plan_id: ID of the plan
            
        Returns:
            List of tasks for the plan
        """
        return [task for task in self.tasks if task["plan_id"] == plan_id]
    
    def update_task(self, task_id: int, status: str) -> Optional[Dict[str, Any]]:
        """
        Update a task's status.
        
        Args:
            task_id: ID of the task to update
            status: New status for the task
            
        Returns:
            Updated task dictionary or None if not found
        """
        task = self.get_task(task_id)
        if task:
            task["status"] = status
            return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if task was deleted, False otherwise
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False