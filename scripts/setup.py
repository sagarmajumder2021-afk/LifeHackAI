#!/usr/bin/env python3
"""
Setup script for LifeHackAI development environment.

This script sets up the development environment, installs dependencies,
initializes the database, and runs basic tests.
"""
import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")

def setup_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("🔄 Creating virtual environment...")
        run_command(f"{sys.executable} -m venv venv", "Virtual environment creation")
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation script path based on OS
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix/Linux/macOS
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    print(f"📝 To activate the virtual environment, run:")
    if os.name == 'nt':
        print(f"   {activate_script}")
    else:
        print(f"   source {activate_script}")
    
    return str(pip_path)

def install_dependencies(pip_path):
    """Install Python dependencies."""
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        run_command(f"{pip_path} install --upgrade pip", "Pip upgrade")
        run_command(f"{pip_path} install -r requirements.txt", "Dependencies installation")
        run_command(f"{pip_path} install pytest pytest-cov", "Test dependencies installation")
    else:
        print("❌ requirements.txt not found")

def initialize_database():
    """Initialize the SQLite database."""
    print("🔄 Initializing database...")
    
    # Import and run database initialization
    sys.path.insert(0, str(Path("backend")))
    try:
        from store import init_db
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

def run_tests():
    """Run the test suite."""
    print("🔄 Running tests...")
    
    # Run tests using pytest
    test_command = "python -m pytest tests/ -v --tb=short"
    result = run_command(test_command, "Test execution")
    
    if result is not None:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")

def create_sample_data():
    """Create sample data for development."""
    print("🔄 Creating sample data...")
    
    try:
        # Add sample problems to database
        db_path = "lifehackai.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if sample data already exists
        cursor.execute("SELECT COUNT(*) FROM problems")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_problems = [
                ("Weekly grocery shopping optimization", "shopping", "Save time and money on groceries while eating healthier"),
                ("Daily productivity routine", "productivity", "Establish a morning routine for better focus and energy"),
                ("Monthly budget planning", "finance", "Create and maintain a personal budget to save more money"),
                ("Home organization system", "home", "Declutter and organize living space for better productivity"),
                ("Healthy meal prep routine", "health", "Plan and prepare nutritious meals for the week")
            ]
            
            cursor.executemany(
                "INSERT INTO problems (title, category, description) VALUES (?, ?, ?)",
                sample_problems
            )
            conn.commit()
            print("✅ Sample data created successfully")
        else:
            print("✅ Sample data already exists")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")

def display_next_steps():
    """Display next steps for the user."""
    print("\n" + "="*60)
    print("🎉 LifeHackAI Setup Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Start the development server:")
    print("   uvicorn backend.main:app --reload --port 8000")
    
    print("\n3. Open your browser and visit:")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Frontend Interface: Open frontend/index.html in your browser")
    
    print("\n4. Try the API endpoints:")
    print("   • GET  /problems - List all problems")
    print("   • POST /problems - Create a new problem")
    print("   • POST /problems/{id}/plan - Generate AI plan")
    
    print("\n5. Run automation scripts:")
    print("   python automation/runners/budget_automation.py")
    print("   python automation/runners/productivity_automation.py")
    
    print("\n6. Run tests:")
    print("   pytest tests/ -v")
    
    print("\n🚀 Happy coding with LifeHackAI!")
    print("="*60)

def main():
    """Main setup function."""
    print("🧠 LifeHackAI Development Environment Setup")
    print("="*50)
    
    # Check Python version
    check_python_version()
    
    # Setup virtual environment
    pip_path = setup_virtual_environment()
    
    # Install dependencies
    install_dependencies(pip_path)
    
    # Initialize database
    initialize_database()
    
    # Create sample data
    create_sample_data()
    
    # Run tests
    run_tests()
    
    # Display next steps
    display_next_steps()

if __name__ == "__main__":
    main()