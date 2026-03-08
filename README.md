# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI web app that uses Google Gemini models to create a personalized 7-day workout plan and a goal-based nutrition or recovery tip. It stores user details, generated plans, and feedback in SQLite. The project provides both REST API endpoints and a clean HTML interface.

## Features

- Generate a 7-day workout plan from user inputs (user_id, goal, intensity)
- Regenerate plans based on feedback ("more cardio", "add rest days")
- Goal-aligned nutrition or recovery tips
- SQLite persistence for users, plans, and feedback
- API endpoints plus a browser-based UI

## Tech Stack

- FastAPI
- SQLite + SQLAlchemy
- Pydantic
- Google Gemini (google-genai)
- Jinja2 templates

## Project Structure

- app/: application package
- app/gemini_generator.py: workout plan generation (Gemini 1.5 Pro, plain-text prompt)
- app/gemini_flash_generator.py: nutrition tip generation (Gemini Flash)
- app/crud.py: database helper functions
- app/database.py: SQLAlchemy engine, session, and Base
- app/main.py: app startup and router wiring
- app/models.py: ORM models (User, Plan, Feedback)
- app/routes.py: all API and UI routes
- app/updated_plan.py: feedback-based plan updater
- app/nutrition.py: goal-based tips
- app/schemas.py: Pydantic request and response models
- app/templates/: HTML templates (index.html, plan.html, result.html, all_users.html)
- app/static/: CSS styles
- requirements.txt: dependencies

## Setup

1) Create and activate a virtual environment.
2) Install dependencies:

```
pip install -r requirements.txt
```

3) Create a .env file (or set environment variables) with your Gemini API key:

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-pro-002
GEMINI_FLASH_MODEL=gemini-1.5-flash-002
```

4) Run the app:

```
uvicorn app.main:app --reload
```

5) Open the UI:

```
http://127.0.0.1:8000/
```

## API Endpoints

### Generate Plan

POST /plans

Request body:

```
{
  "user_id": 101,
  "name": "Alex",
  "age": 24,
  "weight": 68,
  "goal": "weight loss",
  "intensity": "medium"
}
```

Response body (example):

```
{
  "id": 1,
  "user_id": 1,
  "plan": "Day 1:\nWarm-up: ...\nMain Workout: ...\nCooldown: ...\n...",
  "tip": "Aim for a small calorie deficit and include protein at every meal."
}
```

### Submit Feedback (Regenerate Plan)

POST /feedback

Request body:

```
{
  "user_id": 101,
  "feedback": "Add more cardio on Day 2"
}
```

### Get Plan by ID

GET /plans/{plan_id}

### Get User by ID

GET /users/{user_id}

### Get Tip

GET /tips?goal=muscle%20gain

## UI Routes

- GET /: main form page
- POST /generate-workout: create a plan from form input
- POST /submit-feedback: send feedback and regenerate
- GET /view-all-users: admin view of all users

## Notes

- Plans are stored as plain text in SQLite and returned as formatted text.
- Gemini output is plain text (not JSON). If anything fails, a safe fallback plan is used.
- You can change the model via `GEMINI_MODEL` and `GEMINI_FLASH_MODEL` in .env if your account supports different models.
- You can adjust prompts in app/gemini_generator.py and app/updated_plan.py.
- Flash tips are controlled in app/gemini_flash_generator.py.

## Common Issues

- GEMINI_API_KEY missing: set it in .env or your environment.
- Form data error: install python-multipart with `pip install python-multipart`.
- Gemini returns empty output: the app falls back to a default plan.
- SQLite database file is created automatically as fitbuddy.db.

## License

This project is for educational use in the Smart Bridge course.
