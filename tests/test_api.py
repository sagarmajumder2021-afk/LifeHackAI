"""
Tests for the LifeHackAI backend API.
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

client = TestClient(app)

class TestAPI:
    """Test cases for the LifeHackAI API."""
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "LifeHackAI API"
        assert data["status"] == "active"
    
    def test_list_problems(self):
        """Test listing problems."""
        response = client.get("/problems")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 0
    
    def test_create_problem(self):
        """Test creating a new problem."""
        problem_data = {
            "title": "Test Problem",
            "category": "test",
            "description": "This is a test problem"
        }
        response = client.post("/problems", json=problem_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == problem_data["title"]
        assert data["category"] == problem_data["category"]
        assert data["description"] == problem_data["description"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_problem_missing_fields(self):
        """Test creating a problem with missing required fields."""
        problem_data = {
            "title": "Test Problem"
            # Missing category
        }
        response = client.post("/problems", json=problem_data)
        assert response.status_code == 422
    
    def test_get_problem(self):
        """Test getting a specific problem."""
        response = client.get("/problems/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data
        assert "category" in data
    
    def test_get_nonexistent_problem(self):
        """Test getting a problem that doesn't exist."""
        response = client.get("/problems/999")
        assert response.status_code == 404
    
    def test_generate_plan(self):
        """Test generating a plan for a problem."""
        response = client.post("/problems/1/plan")
        assert response.status_code == 200
        data = response.json()
        assert "plan_id" in data
        assert "problem_id" in data
        assert data["problem_id"] == 1
        assert "summary" in data
        assert "steps" in data
        assert isinstance(data["steps"], list)
        assert len(data["steps"]) > 0
        
        # Check step structure
        step = data["steps"][0]
        assert "step_id" in step
        assert "title" in step
        assert "details" in step
        assert "due_offset" in step
    
    def test_generate_plan_nonexistent_problem(self):
        """Test generating a plan for a nonexistent problem."""
        response = client.post("/problems/999/plan")
        assert response.status_code == 404
    
    def test_get_plan(self):
        """Test getting a specific plan."""
        response = client.get("/plans/1")
        assert response.status_code == 200
        data = response.json()
        assert data["plan_id"] == 1
        assert "summary" in data
        assert "steps" in data
    
    def test_create_task(self):
        """Test creating a task from a plan."""
        task_data = {
            "plan_id": 1,
            "title": "Test Task",
            "due_at": "2025-10-22T14:00:00Z"
        }
        response = client.post("/plans/1/tasks", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["plan_id"] == task_data["plan_id"]
        assert data["title"] == task_data["title"]
        assert data["status"] == "pending"
        assert "id" in data
    
    def test_list_tasks(self):
        """Test listing all tasks."""
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_complete_task(self):
        """Test completing a task."""
        # First create a task
        task_data = {
            "plan_id": 1,
            "title": "Task to Complete"
        }
        create_response = client.post("/plans/1/tasks", json=task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        
        # Then complete it
        response = client.post(f"/tasks/{task_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["status"] == "completed"
    
    def test_update_task(self):
        """Test updating a task status."""
        # First create a task
        task_data = {
            "plan_id": 1,
            "title": "Task to Update"
        }
        create_response = client.post("/plans/1/tasks", json=task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        
        # Then update it
        update_data = {"status": "in_progress"}
        response = client.patch(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["status"] == "in_progress"

if __name__ == "__main__":
    pytest.main([__file__])