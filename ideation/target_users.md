FitBuddy Target Users

Primary Demographic:
- Age: 13-90 years old (Validations enforced in backend Pydantic schemas)
- Weight: 30-300 units (Validations enforced in schemas)
- Fitness Level: Beginners to advanced enthusiasts looking for adaptive programming.

Supported Fitness Goals (System Enforced):
1. Weight Loss
2. Muscle Gain
3. General Wellness

Supported Intensities (System Enforced):
1. Low
2. Medium
3. High

User Personas:
1. "The Adaptive Gym-goer": Submits their baseline metrics, receives a 7-day plan, and actively uses the `/submit-feedback` functionality if a particular day's workout was too long or lacked certain exercises.
2. "The Beginner": Uses the system to get a "Low" intensity "General Wellness" plan, relying heavily on the Flash-generated nutrition tips to build better daily habits.

Administrator Persona:
- Uses the `/view-all-users` HTML dashboard to monitor engagement. They can view the `original_plan` and `updated_plan` text strings to ensure the AI is generating safe and accurate changes based on user prompts.
