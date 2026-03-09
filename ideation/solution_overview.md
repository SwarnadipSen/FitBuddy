FitBuddy Solution Overview

Problem:
Individuals often struggle to craft effective, personalized workout routines and nutrition plans that factor in their specific body metrics (age, weight), fitness goals (weight loss, muscle gain, general wellness), and workout intensities. Traditional apps rely on generic, inflexible templates.

Solution:
FitBuddy leverages the google-genai SDK to connect directly with Google Gemini models. It dynamically builds 7-day personalized workout routines and fast, contextual nutrition/recovery tips.

Key Features Built in the Application:
- User Profiles: Captures detailed parameters (name, age 13-90, weight 30-300 lbs/kg, goal, intensity).
- Personalized Plan Generation: Uses `gemini-2.5-flash` (or configured GEMINI_MODEL) to build structured 7-day plans based on the user's specific metrics.
- Targeted Tips: Uses `gemini-2.5-flash` to rapidly generate distinct nutrition or recovery advice alongside the workout.
- NLP Feedback Loop: A dedicated endpoint allows users to say "add more cardio" or "too hard on my knees". The AI interprets this and mutates the existing plan, keeping the good parts while adjusting the requested changes.
- Administrator Dashboard: A UI route (`/view-all-users`) allows admins to see all users, view their original generated plans, and observe how those plans evolved after user feedback.
