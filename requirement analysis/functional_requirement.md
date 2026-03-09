FitBuddy Functional Requirements

1. User Profile Management:
- System must capture and validate via Pydantic: `user_id` (>=1), `name` (1-100 chars), `age` (13-90), `weight` (30-300), `goal` ("weight loss", "muscle gain", "general wellness"), and `intensity` ("low", "medium", "high").
- System must store and retrieve users from the SQLite database.

2. AI Plan Generation (Initial):
- System must generate customized 7-day workout plans using the Gemini AI API (gemini-2.5-flash) specifically tailored to the validated user profile.
- System must concurrently generate specific nutrition/recovery advice using the Gemini Flash API (gemini-2.5-flash) tailored to the user's overarching goal.

3. Interactive Feedback Loop:
- System must parse unstructured natural language user feedback.
- System must inject the feedback and the original plan back into the Gemini AI.
- System must output a newly refined plan that respects the feedback while retaining appropriate structure.
- System must store the feedback iteration in the database associated with that particular plan.

4. UI & Administrative Dashboard:
- System must render Jinja2 HTML templates (`index.html`, `result.html`, `plan.html`) to collect data and securely present the generated AI text.
- System must provide an Admin route `/view-all-users` (rendering `all_users.html`) to display all user metrics, their original AI plans, and their subsequently updated models if feedback was given.
