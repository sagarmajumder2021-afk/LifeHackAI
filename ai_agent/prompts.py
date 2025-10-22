"""
Prompt templates for AI plan generation.
"""

# Base prompt template for problem solving
BASE_PROBLEM_SOLVING_PROMPT = """
You are LifeHackAI, an expert problem-solving assistant that helps people tackle everyday challenges with practical, actionable solutions.

Problem Category: {category}
Problem Title: {title}
Problem Description: {description}

Please generate a comprehensive plan with the following structure:
1. A clear summary of the approach (2-3 sentences)
2. 4-6 specific, actionable steps that are:
   - Practical and achievable
   - Time-bound with realistic deadlines
   - Ordered logically from first to last
   - Specific enough to act on immediately

For each step, provide:
- A clear, action-oriented title
- Detailed instructions on how to complete it
- A realistic time offset (e.g., "0h" for immediate, "2h" for 2 hours later, "1d" for 1 day later)

Focus on solutions that save time, reduce stress, and create lasting positive change.
"""

# Category-specific prompt templates
CATEGORY_PROMPTS = {
    "shopping": """
For shopping-related problems, focus on:
- Time efficiency and cost savings
- Organization and planning strategies
- Smart shopping techniques
- Bulk buying and meal planning
- Price comparison and deal finding
- Reducing food waste
""",
    
    "productivity": """
For productivity-related problems, focus on:
- Time management techniques
- Habit formation and routine building
- Workspace organization
- Focus and concentration strategies
- Energy management throughout the day
- Work-life balance
""",
    
    "finance": """
For finance-related problems, focus on:
- Budgeting and expense tracking
- Saving strategies and goal setting
- Debt management and reduction
- Investment basics for beginners
- Emergency fund building
- Financial habit formation
""",
    
    "health": """
For health-related problems, focus on:
- Sustainable lifestyle changes
- Simple exercise routines
- Nutrition and meal planning
- Sleep hygiene and stress management
- Preventive care and check-ups
- Mental health and well-being
""",
    
    "home": """
For home-related problems, focus on:
- Organization and decluttering
- Maintenance schedules and checklists
- Energy efficiency and cost savings
- Safety and security measures
- DIY solutions for common issues
- Seasonal preparation tasks
"""
}

# Follow-up prompt for plan refinement
REFINEMENT_PROMPT = """
Review the generated plan and ensure it meets these criteria:
1. Each step is specific and actionable
2. Time offsets are realistic and progressive
3. Steps build upon each other logically
4. The plan addresses the root cause, not just symptoms
5. Solutions are practical for the average person
6. The plan can be completed within a reasonable timeframe

If any step is too vague, make it more specific.
If any time offset is unrealistic, adjust it.
If steps are out of order, reorder them logically.
"""

def get_prompt_for_category(category: str, title: str, description: str) -> str:
    """
    Get a customized prompt for a specific problem category.
    
    Args:
        category: Problem category
        title: Problem title
        description: Problem description
        
    Returns:
        Formatted prompt string
    """
    base_prompt = BASE_PROBLEM_SOLVING_PROMPT.format(
        category=category.title(),
        title=title,
        description=description or "No additional description provided."
    )
    
    category_specific = CATEGORY_PROMPTS.get(category.lower(), "")
    
    if category_specific:
        full_prompt = f"{base_prompt}\n\nSpecific guidance for {category} problems:\n{category_specific}"
    else:
        full_prompt = base_prompt
    
    return f"{full_prompt}\n\n{REFINEMENT_PROMPT}"

# Example prompts for testing
EXAMPLE_PROMPTS = {
    "grocery_shopping": get_prompt_for_category(
        "shopping",
        "Weekly grocery shopping optimization",
        "I want to save time and money on my weekly grocery trips while eating healthier."
    ),
    
    "morning_routine": get_prompt_for_category(
        "productivity",
        "Create an effective morning routine",
        "I want to start my day with more energy and focus, but I always feel rushed."
    ),
    
    "budget_planning": get_prompt_for_category(
        "finance",
        "Monthly budget planning",
        "I need to create a budget to track my expenses and save more money each month."
    )
}