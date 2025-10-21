# 🧠 LifeHackAI - Daily Life Problem Solver

LifeHackAI helps solve everyday problems with AI-generated plans, actionable steps, and lightweight automation scripts.

## 🚀 What It Does

LifeHackAI helps normal people tackle daily challenges like:
- ⏰ Time management and productivity
- 💰 Personal budgeting and finance tracking
- 🏠 Home maintenance and organization
- 🧠 Mental well-being and habit formation
- 🛒 Shopping and errands optimization
- 🍽️ Meal planning and nutrition
- 🔧 Basic DIY and troubleshooting

The system generates personalized, step-by-step plans with practical actions and optional automation scripts to make execution easier.

## ✨ Features

- 📋 **Problem Catalog**: Browse common life problems or add your own
- 🤖 **AI Plan Generator**: Get customized step-by-step solutions
- ⏱️ **Task Scheduler**: Convert plans to actionable tasks with reminders
- 🔄 **Lightweight Automation**: Run simple scripts to automate parts of your plan
- 📱 **Simple Interface**: Easy-to-use API and minimal frontend
- 🧩 **Modular Design**: Extensible for different problem domains

## 🛠️ Tech Stack

- **Backend**: Python FastAPI
- **Database**: SQLite (dev), PostgreSQL (prod)
- **AI**: OpenAI API for plan generation
- **Automation**: Python scripts for lightweight task automation
- **Frontend**: Simple HTML/JS (optional React later)
- **Deployment**: Local run + GitHub Actions CI

## 🏗️ Architecture

```
LifeHackAI/
├── docs/                  # Design docs and API specs
├── backend/               # FastAPI application
│   ├── main.py            # Main application entry point
│   ├── models.py          # Pydantic data models
│   ├── api.py             # API endpoints
│   ├── plans.py           # AI plan generation logic
│   ├── tasks.py           # Task scheduler
│   └── store.py           # Database access
├── automation/            # Automation scripts
│   ├── runners/           # Script runners for common tasks
│   └── adapters/          # Adapters for external services
├── ai_agent/              # AI agent components
│   ├── agent.py           # Main orchestrator
│   └── prompts/           # Prompt templates
├── frontend/              # Simple frontend (optional)
├── scripts/               # Utility scripts
└── tests/                 # Test suite
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/sagarmajumder2021-afk/LifeHackAI.git
cd LifeHackAI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn backend.main:app --reload --port 8000
```

### Using the API

1. **Create a problem**:
   ```
   POST /problems
   {
     "title": "I need to organize my weekly grocery shopping",
     "category": "shopping",
     "description": "I want to save time and money on groceries"
   }
   ```

2. **Generate a plan**:
   ```
   POST /problems/{problem_id}/plan
   ```

3. **Create tasks from the plan**:
   ```
   POST /plans/{plan_id}/tasks
   ```

4. **Mark tasks as complete**:
   ```
   POST /tasks/{task_id}/complete
   ```

## 🧩 Extending LifeHackAI

### Adding New Problem Domains

1. Create a new module in `automation/runners/`
2. Add domain-specific prompts in `ai_agent/prompts/`
3. Register the new domain in the problem catalog

### Creating Custom Automation Scripts

1. Add your script to `automation/runners/`
2. Ensure it follows the standard interface
3. Register it in the automation registry

## 📝 License

MIT License © 2025 Sagar Majumder

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ by [Sagar Majumder](https://github.com/sagarmajumder2021-afk)**