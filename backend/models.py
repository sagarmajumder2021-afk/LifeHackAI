"""
Pydantic models for LifeHackAI.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Problem Models
class ProblemCreate(BaseModel):
    """Model for creating a new problem."""
    title: str = Field(..., description="Title of the problem", min_length=5, max_length=100)
    category: str = Field(..., description="Category of the problem", min_length=3, max_length=50)
    description: Optional[str] = Field(None, description="Detailed description of the problem")

class ProblemResponse(BaseModel):
    """Model for problem response."""
    id: int = Field(..., description="Unique identifier for the problem")
    title: str = Field(..., description="Title of the problem")
    category: str = Field(..., description="Category of the problem")
    description: Optional[str] = Field(None, description="Detailed description of the problem")
    created_at: str = Field(..., description="Creation timestamp")

# Plan Models
class PlanStep(BaseModel):
    """Model for a step in a plan."""
    step_id: int = Field(..., description="Unique identifier for the step within the plan")
    title: str = Field(..., description="Title of the step")
    details: str = Field(..., description="Detailed description of the step")
    due_offset: str = Field(..., description="Time offset for due date (e.g., '2h', '1d')")

class PlanResponse(BaseModel):
    """Model for plan response."""
    plan_id: int = Field(..., description="Unique identifier for the plan")
    problem_id: int = Field(..., description="ID of the problem this plan addresses")
    generated_at: str = Field(..., description="Generation timestamp")
    summary: str = Field(..., description="Summary of the plan")
    steps: List[PlanStep] = Field(..., description="Steps in the plan")

# Task Models
class TaskCreate(BaseModel):
    """Model for creating a new task."""
    plan_id: int = Field(..., description="ID of the plan this task belongs to")
    title: Optional[str] = Field(None, description="Title of the task")
    due_at: Optional[str] = Field(None, description="Due date and time (ISO format)")

class TaskUpdate(BaseModel):
    """Model for updating a task."""
    status: str = Field(..., description="New status for the task", pattern="^(pending|in_progress|completed)$")

class TaskResponse(BaseModel):
    """Model for task response."""
    id: int = Field(..., description="Unique identifier for the task")
    plan_id: int = Field(..., description="ID of the plan this task belongs to")
    title: str = Field(..., description="Title of the task")
    due_at: str = Field(..., description="Due date and time (ISO format)")
    status: str = Field(..., description="Status of the task (pending, in_progress, completed)")

# User Models (for future use)
class UserPreferences(BaseModel):
    """Model for user preferences."""
    timezone: str = Field("UTC", description="User's timezone")
    notification_method: str = Field("email", description="Preferred notification method")

class UserCreate(BaseModel):
    """Model for creating a new user."""
    name: str = Field(..., description="User's name")
    email: str = Field(..., description="User's email")
    preferences: Optional[UserPreferences] = Field(None, description="User preferences")

class UserResponse(BaseModel):
    """Model for user response."""
    id: int = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="User's name")
    email: str = Field(..., description="User's email")
    preferences: UserPreferences = Field(..., description="User preferences")
    created_at: str = Field(..., description="Creation timestamp")