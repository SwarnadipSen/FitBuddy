import os
from typing import Dict

from dotenv import load_dotenv
from google import genai
from google.genai import errors
import json

def _get_client() -> genai.Client:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return genai.Client(api_key=api_key, http_options={"api_version": "v1"})


def _get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-1.5-pro-002")


def fallback_plan(goal: str, intensity: str) -> str:
    return (
        "Day 1:\nWarm-up: 5-10 minutes brisk walk and dynamic stretches\n"
        "Main Workout: Squats 3x12, Push-ups 3x10, Plank 2 minutes\n"
        "Cooldown: 5 minutes light stretching\n\n"
        "Day 2:\nWarm-up: 5 minutes light jog\n"
        "Main Workout: Brisk walk 20 minutes, Cycling 10 minutes\n"
        "Cooldown: Breathing and calf stretches\n\n"
        "Day 3:\nWarm-up: Gentle mobility flow\n"
        "Main Workout: Recovery stretch 10 minutes\n"
        "Cooldown: Hydrate and relax\n\n"
        "Day 4:\nWarm-up: Arm circles and band pulls\n"
        "Main Workout: Dumbbell rows 3x12, Shoulder press 3x10\n"
        "Cooldown: Chest and shoulder stretches\n\n"
        "Day 5:\nWarm-up: Leg swings and hip openers\n"
        "Main Workout: Lunges 3x12, Glute bridges 3x15\n"
        "Cooldown: Hamstring stretch\n\n"
        "Day 6:\nWarm-up: March in place 5 minutes\n"
        "Main Workout: Jogging 20 minutes, Bicycle crunches 3x15\n"
        "Cooldown: Core stretch and breathing\n\n"
        "Day 7:\nWarm-up: Gentle mobility flow\n"
        "Main Workout: Light yoga 15 minutes\n"
        "Cooldown: Relaxation and hydration"
    )



def generate_workout_gemini(
    *, name: str, age: int, weight: int, goal: str, intensity: str
) -> str:
    client = _get_client()
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of {goal}, and prefers {intensity} intensity workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)

User details: name={name}, age={age}, weight={weight}.
"""
    try:
        response = client.models.generate_content(
            model=_get_model_name(),
            contents=prompt,
        )
        return response.text.strip() if getattr(response, "text", None) else fallback_plan(goal, intensity)
    except (json.JSONDecodeError, errors.ClientError, errors.ServerError):
        return fallback_plan(goal, intensity)
