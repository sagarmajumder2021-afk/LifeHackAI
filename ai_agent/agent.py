"""
Main AI agent orchestrator for LifeHackAI.

This module coordinates between plan generation, task creation, and automation execution.
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from ..backend.plans import generate_plan, parse_due_offset
from ..backend.tasks import TaskManager
from ..automation.runners.budget_automation import create_budget_snapshot, analyze_budget
from ..automation.runners.productivity_automation import create_daily_schedule, set_focus_timer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LifeHackAgent:
    """
    Main AI agent that orchestrates problem-solving workflows.
    
    This agent can:
    1. Generate AI plans for problems
    2. Create tasks from plans
    3. Execute automation scripts
    4. Provide recommendations
    """
    
    def __init__(self):
        """Initialize the LifeHack agent."""
        self.task_manager = TaskManager()
        self.automation_registry = {
            "budget": {
                "create_snapshot": create_budget_snapshot,
                "analyze": analyze_budget
            },
            "productivity": {
                "create_schedule": create_daily_schedule,
                "focus_timer": set_focus_timer
            }
        }
        logger.info("LifeHack AI Agent initialized")
    
    def solve_problem(self, problem_id: int, auto_create_tasks: bool = True) -> Dict[str, Any]:
        """
        Complete problem-solving workflow.
        
        Args:
            problem_id: ID of the problem to solve
            auto_create_tasks: Whether to automatically create tasks from the plan
            
        Returns:
            Dictionary containing the complete solution
        """
        logger.info(f"Starting problem-solving workflow for problem {problem_id}")
        
        # Step 1: Generate AI plan
        plan = generate_plan(problem_id)
        logger.info(f"Generated plan with {len(plan['steps'])} steps")
        
        # Step 2: Create tasks if requested
        tasks = []
        if auto_create_tasks:
            tasks = self._create_tasks_from_plan(plan)
            logger.info(f"Created {len(tasks)} tasks from plan")
        
        # Step 3: Identify automation opportunities
        automation_suggestions = self._suggest_automations(plan)
        
        # Step 4: Create solution summary
        solution = {
            "problem_id": problem_id,
            "plan": plan,
            "tasks": tasks,
            "automation_suggestions": automation_suggestions,
            "workflow_completed_at": datetime.now().isoformat(),
            "next_steps": self._generate_next_steps(plan, tasks)
        }
        
        logger.info("Problem-solving workflow completed successfully")
        return solution
    
    def _create_tasks_from_plan(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create tasks from plan steps.
        
        Args:
            plan: Plan dictionary with steps
            
        Returns:
            List of created tasks
        """
        tasks = []
        base_time = datetime.now()
        
        for step in plan["steps"]:
            # Calculate due time based on offset
            offset_minutes = parse_due_offset(step["due_offset"])
            due_time = base_time + timedelta(minutes=offset_minutes)
            
            # Create task
            task_id = self.task_manager.add_task(
                plan_id=plan["plan_id"],
                title=step["title"],
                due_at=due_time.isoformat()
            )
            
            task = self.task_manager.get_task(task_id)
            tasks.append(task)
        
        return tasks
    
    def _suggest_automations(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest automation scripts based on the plan.
        
        Args:
            plan: Plan dictionary
            
        Returns:
            List of automation suggestions
        """
        suggestions = []
        
        # Check for budget-related steps
        budget_keywords = ["budget", "money", "expense", "cost", "financial"]
        if any(keyword in plan["summary"].lower() for keyword in budget_keywords):
            suggestions.append({
                "type": "budget",
                "script": "create_snapshot",
                "description": "Create a budget snapshot to track your finances",
                "estimated_time_saved": "30 minutes"
            })
        
        # Check for productivity-related steps
        productivity_keywords = ["schedule", "time", "productivity", "routine", "organize"]
        if any(keyword in plan["summary"].lower() for keyword in productivity_keywords):
            suggestions.append({
                "type": "productivity",
                "script": "create_schedule",
                "description": "Create a daily schedule to optimize your time",
                "estimated_time_saved": "15 minutes daily"
            })
        
        return suggestions
    
    def _generate_next_steps(self, plan: Dict[str, Any], tasks: List[Dict[str, Any]]) -> List[str]:
        """
        Generate recommended next steps for the user.
        
        Args:
            plan: Plan dictionary
            tasks: List of tasks
            
        Returns:
            List of next step recommendations
        """
        next_steps = []
        
        if tasks:
            # Find the first pending task
            pending_tasks = [t for t in tasks if t["status"] == "pending"]
            if pending_tasks:
                first_task = min(pending_tasks, key=lambda x: x["due_at"])
                next_steps.append(f"Start with: {first_task['title']}")
        
        # Add general recommendations
        next_steps.extend([
            "Review all tasks and their due dates",
            "Set up reminders for important deadlines",
            "Consider running suggested automation scripts",
            "Track your progress and adjust the plan as needed"
        ])
        
        return next_steps
    
    def execute_automation(self, automation_type: str, script_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute an automation script.
        
        Args:
            automation_type: Type of automation (budget, productivity, etc.)
            script_name: Name of the script to run
            **kwargs: Additional parameters for the script
            
        Returns:
            Result of the automation execution
        """
        logger.info(f"Executing automation: {automation_type}.{script_name}")
        
        if automation_type not in self.automation_registry:
            raise ValueError(f"Unknown automation type: {automation_type}")
        
        if script_name not in self.automation_registry[automation_type]:
            raise ValueError(f"Unknown script: {script_name} for type {automation_type}")
        
        try:
            script_function = self.automation_registry[automation_type][script_name]
            result = script_function(**kwargs)
            
            execution_result = {
                "automation_type": automation_type,
                "script_name": script_name,
                "parameters": kwargs,
                "result": result,
                "status": "success",
                "executed_at": datetime.now().isoformat()
            }
            
            logger.info(f"Automation executed successfully: {automation_type}.{script_name}")
            return execution_result
            
        except Exception as e:
            logger.error(f"Automation execution failed: {e}")
            return {
                "automation_type": automation_type,
                "script_name": script_name,
                "parameters": kwargs,
                "error": str(e),
                "status": "failed",
                "executed_at": datetime.now().isoformat()
            }
    
    def get_user_dashboard(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate a user dashboard with current status and recommendations.
        
        Args:
            user_id: User ID (for future use)
            
        Returns:
            Dashboard data
        """
        all_tasks = self.task_manager.get_all_tasks()
        
        # Calculate task statistics
        pending_tasks = [t for t in all_tasks if t["status"] == "pending"]
        completed_tasks = [t for t in all_tasks if t["status"] == "completed"]
        overdue_tasks = []
        
        now = datetime.now()
        for task in pending_tasks:
            task_due = datetime.fromisoformat(task["due_at"])
            if task_due < now:
                overdue_tasks.append(task)
        
        # Generate recommendations
        recommendations = []
        if overdue_tasks:
            recommendations.append(f"You have {len(overdue_tasks)} overdue tasks. Consider rescheduling or completing them.")
        if len(pending_tasks) > 10:
            recommendations.append("You have many pending tasks. Consider prioritizing the most important ones.")
        if not pending_tasks:
            recommendations.append("Great job! You have no pending tasks. Consider creating a new plan for your next goal.")
        
        dashboard = {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "task_summary": {
                "total_tasks": len(all_tasks),
                "pending_tasks": len(pending_tasks),
                "completed_tasks": len(completed_tasks),
                "overdue_tasks": len(overdue_tasks)
            },
            "upcoming_tasks": sorted(pending_tasks, key=lambda x: x["due_at"])[:5],
            "recent_completions": sorted(completed_tasks, key=lambda x: x.get("completed_at", ""), reverse=True)[:3],
            "recommendations": recommendations
        }
        
        return dashboard

# Global agent instance
agent = LifeHackAgent()