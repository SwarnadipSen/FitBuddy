from typing import Dict

from google.genai import errors

from .gemini_generator import _get_client, _get_model_name



def update_workout_plan(
    *, current_plan: str, feedback: str, goal: str, intensity: str
) -> str:
    client = _get_client()
    prompt = (
        "You are a fitness coach. Update the given 7-day plan based on feedback. "
        f"Goal={goal}, intensity={intensity}. Feedback: {feedback}. "
        f"Here is the original plan:\n{current_plan}\n"
        "Keep the same format and update only what is needed."
    )
    try:
        response = client.models.generate_content(
            model=_get_model_name(),
            contents=prompt,
        )
        return response.text.strip() if getattr(response, "text", None) else current_plan
    except (errors.ClientError, errors.ServerError):
        return current_plan
