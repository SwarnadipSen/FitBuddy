FitBuddy Model & Technology Selection

Primary AI Provider: Google Gemini API (via google-genai SDK)

1. Unified AI Model (gemini-2.5-flash by default):
- Primary Use: Workout Generation, Plan Updating, and Nutrition/Recovery Tips.
- Rationale: Google's Gemini 2.5 Flash model provides an excellent balance of high-speed response times and complex reasoning capabilities. It is more than capable of handling the multi-variable prompts required for 7-day structured workout routines and safely integrating unstructured user feedback, while being fast enough to rapidly generate the accompanying short-form nutrition and recovery tips without causing undue latency for the user. Both GEMINI_MODEL and GEMINI_FLASH_MODEL point to this single, performant model.

Tech Stack Details:
- Framework: FastAPI (Python) for robust, async-capable HTTP routing and Pydantic validation (e.g., age max 90, weight max 300).
- Database: SQLite (local) via SQLAlchemy ORM. Keeps track of User profiles, relational Plans (1:M with Users), and Feedback histories (1:M with Plans) so the AI context can be loaded directly from DB.
- Frontend Layer: HTML templates rendered via Jinja2, utilizing Tailwind CSS compiled through PostCSS for scalable, utility-first styling.
