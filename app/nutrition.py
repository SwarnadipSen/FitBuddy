def get_tip(goal: str) -> str:
    tips = {
        "weight loss": "Aim for a small calorie deficit and include protein at every meal.",
        "muscle gain": "Include 20-30g protein within an hour after training.",
        "general wellness": "Prioritize sleep and hydrate regularly throughout the day.",
    }
    return tips.get(goal, "Stay consistent with balanced meals and recovery.")
