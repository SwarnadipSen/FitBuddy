from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

GoalType = Literal["weight loss", "muscle gain", "general wellness"]
IntensityType = Literal["low", "medium", "high"]



class UserInput(BaseModel):
	user_id: int = Field(..., ge=1)
	name: str = Field(..., min_length=1, max_length=100)
	age: int = Field(..., ge=13, le=90)
	weight: int = Field(..., ge=30, le=300)
	goal: GoalType
	intensity: IntensityType


class UserResponse(UserInput):
	model_config = ConfigDict(from_attributes=True)

	id: int


class PlanRequest(UserInput):
	pass


class PlanResponse(BaseModel):
	id: int
	user_id: int
	plan: str
	tip: Optional[str] = None

	model_config = ConfigDict(from_attributes=True)


class FeedbackRequest(BaseModel):
	user_id: int = Field(..., ge=1)
	feedback: str = Field(..., min_length=3, max_length=500)


class FeedbackResponse(BaseModel):
	id: int
	plan_id: int
	comment: str

	model_config = ConfigDict(from_attributes=True)


class TipResponse(BaseModel):
	goal: GoalType
	tip: str
