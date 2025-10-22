# Contributing to LifeHackAI

Thank you for your interest in contributing to LifeHackAI! 🎉

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of FastAPI, Python, and web development

### Setup Development Environment
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/LifeHackAI.git
   cd LifeHackAI
   ```
3. Run the setup script:
   ```bash
   python scripts/setup.py
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## 🛠️ Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow the existing code style and patterns
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest --cov=./ --cov-report=html
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Write descriptive docstrings for functions and classes
- Keep functions focused and small

### Example:
```python
def generate_plan(problem_id: int) -> Dict[str, Any]:
    """
    Generate an AI plan for a given problem.
    
    Args:
        problem_id: ID of the problem to generate a plan for
        
    Returns:
        Dictionary containing the plan details
    """
    # Implementation here
    pass
```

### API Endpoints
- Use RESTful conventions
- Include proper error handling
- Add comprehensive docstrings
- Validate input data with Pydantic models

### Frontend Code
- Use semantic HTML
- Follow responsive design principles
- Add proper error handling for API calls
- Keep JavaScript functions small and focused

## 🧪 Testing Guidelines

### Writing Tests
- Write tests for all new functionality
- Include both positive and negative test cases
- Test edge cases and error conditions
- Aim for high test coverage

### Test Structure
```python
class TestYourFeature:
    """Test cases for your feature."""
    
    def test_positive_case(self):
        """Test the happy path."""
        # Test implementation
        pass
    
    def test_error_case(self):
        """Test error handling."""
        # Test implementation
        pass
```

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Include parameter descriptions and return types
- Provide usage examples where helpful

### API Documentation
- Update API documentation for new endpoints
- Include request/response examples
- Document error codes and messages

## 🎯 Types of Contributions

### 🐛 Bug Fixes
- Fix existing issues
- Add tests to prevent regression
- Update documentation if needed

### ✨ New Features
- Add new automation scripts
- Implement new problem categories
- Enhance the AI agent capabilities
- Improve the frontend interface

### 📖 Documentation
- Improve existing documentation
- Add tutorials and examples
- Fix typos and clarify instructions

### 🧪 Testing
- Add missing tests
- Improve test coverage
- Add integration tests

## 🔄 Automation Scripts

### Adding New Automation Scripts
1. Create a new file in `automation/runners/`
2. Follow the existing pattern:
   ```python
   def your_automation_function(**kwargs) -> Dict[str, Any]:
       """
       Your automation function description.
       
       Args:
           **kwargs: Function parameters
           
       Returns:
           Dictionary with automation results
       """
       # Implementation
       pass
   ```
3. Add tests in `tests/test_automation.py`
4. Register the script in `ai_agent/agent.py`

### Problem Categories
When adding new problem categories:
1. Add category-specific prompts in `ai_agent/prompts.py`
2. Create sample plans in `backend/plans.py`
3. Add corresponding automation scripts if applicable

## 🚀 Deployment Contributions

### Docker Support
- Help improve Docker configuration
- Add docker-compose for development
- Optimize container size and performance

### Cloud Deployment
- Add deployment guides for various platforms
- Create infrastructure as code templates
- Improve CI/CD pipeline

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

## 🤝 Community Guidelines

### Be Respectful
- Use inclusive language
- Be constructive in feedback
- Help others learn and grow

### Communication
- Ask questions if unclear
- Provide context in issues and PRs
- Be patient with review process

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks in documentation

## 📞 Getting Help

- 📧 Email: sagarm.work@gmail.com
- 💬 GitHub Issues: For bugs and feature requests
- 📖 Documentation: Check existing docs first

Thank you for contributing to LifeHackAI! 🚀