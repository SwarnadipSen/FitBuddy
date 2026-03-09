FitBuddy System Planning

Architecture Outline:
- Core Backend Framework: FastAPI (Python) - Handles async async/sync endpoint routing.
- Database ORM: SQLAlchemy connecting to a local SQLite (`fitbuddy.db`).
- Database Setup: Managed via `database.py` (engine and declarative_base declarations).
- UI Templating: Jinja2 Templates mapped to the `/templates` directory.
- Static Files: Mounted `/static` directory serving Tailwind CSS stylesheets built via PostCSS.

Component Layout:
- `main.py`: Bootstraps the FastAPI instance, creates DB tables, mounts routers and statics.
- `routes.py`: Defines GET/POST REST APIs (`/plans`, `/feedback`, `/tips`) and GET/POST UI routes (`/`, `/generate-workout`, `/submit-feedback`).
- `schemas.py`: Heavily utilized Pydantic BaseModel validaton rules ensure LLM prompts are safe.
- `models.py`: SQLAlchemy relations (`User` has many `Plan`, `Plan` has many `Feedback`).
- `crud.py`: Houses all DB query abstractions (upserts, selects, plan retrieval).
- `gemini_generator.py` & `updated_plan.py`: Houses the prompt-engineering definitions and SDK calls to `gemini-2.5-flash` for building/updating workouts.
- `gemini_flash_generator.py`: Fast-response SDK calls to `gemini-2.5-flash` for static tips.

Infrastructure Requirements:
- Python Virtual Environment with `requirements.txt` installed.
- Environment variables configured via `.env` (GEMINI_API_KEY, GEMINI_MODEL, GEMINI_FLASH_MODEL).
