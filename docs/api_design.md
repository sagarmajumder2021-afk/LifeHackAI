# API Design Document

## Overview
This document outlines the API design for LifeHackAI, a system that helps solve everyday problems with AI-generated plans, actionable steps, and lightweight automation scripts.

## Base URL
```
http://localhost:8000
```

## Authentication
Authentication is not implemented in the MVP but will be added in future versions using JWT tokens.

## API Endpoints

### Problems

#### GET /problems
List all available problems.

**Response**
```json
[
  {
    "id": 1,
    "title": "Weekly grocery shopping optimization",
    "category": "shopping",
    "description": "Save time and money on groceries",
    "created_at": "2025-10-21T12:00:00Z"
  },
  {
    "id": 2,
    "title": "Daily productivity routine",
    "category": "productivity",
    "description": "Establish a morning routine for better productivity",
    "created_at": "2025-10-21T12:00:00Z"
  }
]
```

#### POST /problems
Create a new problem.

**Request**
```json
{
  "title": "Monthly budget planning",
  "category": "finance",
  "description": "Create and stick to a personal budget"
}
```

**Response**
```json
{
  "id": 3,
  "title": "Monthly budget planning",
  "category": "finance",
  "description": "Create and stick to a personal budget",
  "created_at": "2025-10-21T12:00:00Z"
}
```

#### GET /problems/{problem_id}
Get a specific problem by ID.

**Response**
```json
{
  "id": 1,
  "title": "Weekly grocery shopping optimization",
  "category": "shopping",
  "description": "Save time and money on groceries",
  "created_at": "2025-10-21T12:00:00Z"
}
```

### Plans

#### POST /problems/{problem_id}/plan
Generate an AI plan for a specific problem.

**Response**
```json
{
  "plan_id": 1,
  "problem_id": 1,
  "generated_at": "2025-10-21T12:00:00Z",
  "summary": "Optimize your weekly grocery shopping to save time and money",
  "steps": [
    {
      "step_id": 1,
      "title": "Create a meal plan",
      "details": "Plan your meals for the week to know exactly what you need",
      "due_offset": "0h"
    },
    {
      "step_id": 2,
      "title": "Take inventory",
      "details": "Check what you already have to avoid buying duplicates",
      "due_offset": "1h"
    }
  ]
}
```

#### GET /plans/{plan_id}
Get a specific plan by ID.

**Response**
```json
{
  "plan_id": 1,
  "problem_id": 1,
  "generated_at": "2025-10-21T12:00:00Z",
  "summary": "Optimize your weekly grocery shopping to save time and money",
  "steps": [
    {
      "step_id": 1,
      "title": "Create a meal plan",
      "details": "Plan your meals for the week to know exactly what you need",
      "due_offset": "0h"
    },
    {
      "step_id": 2,
      "title": "Take inventory",
      "details": "Check what you already have to avoid buying duplicates",
      "due_offset": "1h"
    }
  ]
}
```

### Tasks

#### POST /plans/{plan_id}/tasks
Create a new task from a plan.

**Request**
```json
{
  "plan_id": 1,
  "title": "Create a meal plan",
  "due_at": "2025-10-21T14:00:00Z"
}
```

**Response**
```json
{
  "id": 1,
  "plan_id": 1,
  "title": "Create a meal plan",
  "due_at": "2025-10-21T14:00:00Z",
  "status": "pending"
}
```

#### GET /tasks
List all tasks.

**Response**
```json
[
  {
    "id": 1,
    "plan_id": 1,
    "title": "Create a meal plan",
    "due_at": "2025-10-21T14:00:00Z",
    "status": "pending"
  },
  {
    "id": 2,
    "plan_id": 1,
    "title": "Take inventory",
    "due_at": "2025-10-21T15:00:00Z",
    "status": "pending"
  }
]
```

#### GET /tasks/{task_id}
Get a specific task by ID.

**Response**
```json
{
  "id": 1,
  "plan_id": 1,
  "title": "Create a meal plan",
  "due_at": "2025-10-21T14:00:00Z",
  "status": "pending"
}
```

#### PATCH /tasks/{task_id}
Update a task's status.

**Request**
```json
{
  "status": "completed"
}
```

**Response**
```json
{
  "id": 1,
  "plan_id": 1,
  "title": "Create a meal plan",
  "due_at": "2025-10-21T14:00:00Z",
  "status": "completed"
}
```

#### POST /tasks/{task_id}/complete
Mark a task as complete.

**Response**
```json
{
  "id": 1,
  "plan_id": 1,
  "title": "Create a meal plan",
  "due_at": "2025-10-21T14:00:00Z",
  "status": "completed"
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Future Endpoints

### Users
- POST /users - Create a new user
- GET /users/me - Get current user
- PATCH /users/me - Update current user
- GET /users/me/problems - Get current user's problems
- GET /users/me/plans - Get current user's plans
- GET /users/me/tasks - Get current user's tasks

### Automation
- POST /automation/run - Run an automation script
- GET /automation/scripts - List available automation scripts
- GET /automation/runs - List automation script runs