FitBuddy Project Workflow

1. Data Ingestion:
- Endpoint: Frontend Form (GET `/`) submits to POST `/generate-workout` (or API POST `/plans`).
- Action: Data passes through Pydantic `PlanRequest` schema validation.
- Database: `crud.upsert_user` checks for existing `external_id`, creating or updating the User record in SQLite.

2. Parallel AI Execution:
- Action 1: `gemini_generator.generate_workout_gemini` formulates the prompt combining Name, Age, Weight, Goal, and Intensity, and calls the Gemini Pro model to get a 7-day text plan.
- Action 2: `gemini_flash_generator.generate_nutrition_tip_with_flash` passes the Goal variable to Gemini Flash to receive a targeted tip.
- Database: `crud.create_plan` creates a new linked `Plan` entity storing both AI responses.

3. Frontend Rendering:
- Action: FastAPI renders `result.html` containing the injected AI text, formatting it visually for the end-user.

4. Feedback Submission (Self-Correction Loop):
- Endpoint: POST `/submit-feedback` (UI) or POST `/feedback` (API).
- Database: Validates existence of user and their latest `Plan`.
- Action: `updated_plan.update_workout_plan` takes the `current_plan` string, the new `feedback` string, and core goals. It prompts Gemini Pro to specifically modify the workout.
- Database: `crud.update_plan` overwrites the `updated_plan` column, and `crud.create_feedback` logs the actual feedback text.
- Render: `result.html` is returned with the new AI-generated text.

5. Analytics / Oversight:
- Endpoint: GET `/view-all-users`.
- Action: Selects all Users and eagerly attempts to fetch their latest Plans to tabulate differences between `original_plan` and `updated_plan`.
