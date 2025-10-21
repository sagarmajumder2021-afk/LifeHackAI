"""
Database access module for LifeHackAI.
"""
import os
import sqlite3
from typing import Dict, List, Any, Optional
from contextlib import contextmanager

# Database file path
DB_PATH = os.environ.get("DB_PATH", "lifehackai.db")

def init_db():
    """
    Initialize the database with required tables.
    
    In a production app, this would use SQLAlchemy or another ORM.
    For demo purposes, we're using SQLite directly.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Create problems table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create plans table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            summary TEXT NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (problem_id) REFERENCES problems (id)
        )
        """)
        
        # Create plan_steps table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plan_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER NOT NULL,
            step_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            details TEXT NOT NULL,
            due_offset TEXT NOT NULL,
            FOREIGN KEY (plan_id) REFERENCES plans (id)
        )
        """)
        
        # Create tasks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            due_at TIMESTAMP NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (plan_id) REFERENCES plans (id)
        )
        """)
        
        # Insert sample data if tables are empty
        cursor.execute("SELECT COUNT(*) FROM problems")
        if cursor.fetchone()[0] == 0:
            insert_sample_data(conn)
        
        conn.commit()

def insert_sample_data(conn):
    """
    Insert sample data into the database.
    
    Args:
        conn: Database connection
    """
    cursor = conn.cursor()
    
    # Insert sample problems
    problems = [
        ("Weekly grocery shopping optimization", "shopping", "Save time and money on groceries"),
        ("Daily productivity routine", "productivity", "Establish a morning routine for better productivity"),
        ("Monthly budget planning", "finance", "Create and stick to a personal budget")
    ]
    
    cursor.executemany(
        "INSERT INTO problems (title, category, description) VALUES (?, ?, ?)",
        problems
    )
    
    conn.commit()

@contextmanager
def get_connection():
    """
    Context manager for database connections.
    
    Yields:
        SQLite connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_db():
    """
    Get database connection for dependency injection.
    
    In a real FastAPI app, this would be used with Depends().
    For demo purposes, it's simplified.
    
    Returns:
        Database connection
    """
    with get_connection() as conn:
        yield conn