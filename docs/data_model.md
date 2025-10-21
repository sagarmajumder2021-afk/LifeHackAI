# Data Model Design

## Overview
This document outlines the data model design for LifeHackAI, a system that helps solve everyday problems with AI-generated plans, actionable steps, and lightweight automation scripts.

## Entities

### Problem
Represents a daily life problem that needs to be solved.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Title of the problem |
| category | String | Category of the problem (e.g., shopping, productivity, finance) |
| description | String | Detailed description of the problem |
| created_at | DateTime | Creation timestamp |
| user_id | Integer | Foreign key to User (future) |

### Plan
Represents an AI-generated plan to solve a problem.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| problem_id | Integer | Foreign key to Problem |
| summary | String | Summary of the plan |
| generated_at | DateTime | Generation timestamp |
| user_id | Integer | Foreign key to User (future) |

### PlanStep
Represents a step in a plan.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| plan_id | Integer | Foreign key to Plan |
| step_id | Integer | Identifier for the step within the plan |
| title | String | Title of the step |
| details | String | Detailed description of the step |
| due_offset | String | Time offset for due date (e.g., '2h', '1d') |

### Task
Represents a task created from a plan step.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| plan_id | Integer | Foreign key to Plan |
| title | String | Title of the task |
| due_at | DateTime | Due date and time |
| status | String | Status of the task (pending, in_progress, completed) |
| user_id | Integer | Foreign key to User (future) |

### User (Future)
Represents a user of the system.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | User's name |
| email | String | User's email |
| password_hash | String | Hashed password |
| created_at | DateTime | Creation timestamp |

### UserPreferences (Future)
Represents user preferences.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| timezone | String | User's timezone |
| notification_method | String | Preferred notification method |

### AutomationRun (Future)
Represents a run of an automation script.

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| script_name | String | Name of the script |
| parameters | JSON | Parameters passed to the script |
| result | JSON | Result of the script run |
| status | String | Status of the run (success, failure) |
| created_at | DateTime | Creation timestamp |

## Relationships

- A **User** can have many **Problems**
- A **Problem** belongs to a **User**
- A **Problem** can have many **Plans**
- A **Plan** belongs to a **Problem**
- A **Plan** belongs to a **User**
- A **Plan** can have many **PlanSteps**
- A **PlanStep** belongs to a **Plan**
- A **Plan** can have many **Tasks**
- A **Task** belongs to a **Plan**
- A **Task** belongs to a **User**
- A **User** has one **UserPreferences**
- A **UserPreferences** belongs to a **User**
- A **User** can have many **AutomationRuns**
- An **AutomationRun** belongs to a **User**

## Database Schema (SQLite)

```sql
CREATE TABLE problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER
);

CREATE TABLE plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER NOT NULL,
    summary TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (problem_id) REFERENCES problems (id)
);

CREATE TABLE plan_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    step_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    details TEXT NOT NULL,
    due_offset TEXT NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES plans (id)
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    due_at TIMESTAMP NOT NULL,
    status TEXT DEFAULT 'pending',
    user_id INTEGER,
    FOREIGN KEY (plan_id) REFERENCES plans (id)
);

-- Future tables

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timezone TEXT DEFAULT 'UTC',
    notification_method TEXT DEFAULT 'email',
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE automation_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    script_name TEXT NOT NULL,
    parameters TEXT,
    result TEXT,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## Data Flow

1. User creates a **Problem**
2. System generates a **Plan** with multiple **PlanSteps**
3. User converts **PlanSteps** into **Tasks**
4. User completes **Tasks**
5. User runs **AutomationScripts** to help with tasks

## Future Considerations

- Add support for recurring tasks
- Implement task dependencies
- Add task priorities
- Support for collaborative plans and tasks
- Integration with external calendars and task managers