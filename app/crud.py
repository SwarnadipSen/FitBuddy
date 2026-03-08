import json
from datetime import datetime

from sqlalchemy.orm import Session

from . import models
from . import schemas


def upsert_user(db: Session, user_in: schemas.UserInput) -> models.User:
	user = (
		db.query(models.User)
		.filter(models.User.external_id == user_in.user_id)
		.first()
	)
	if user:
		user.name = user_in.name.strip()
		user.age = user_in.age
		user.weight = user_in.weight
		user.goal = user_in.goal
		user.intensity = user_in.intensity
	else:
		user = models.User(
			external_id=user_in.user_id,
			name=user_in.name.strip(),
			age=user_in.age,
			weight=user_in.weight,
			goal=user_in.goal,
			intensity=user_in.intensity,
		)
		db.add(user)
	db.commit()
	db.refresh(user)
	return user


def get_user(db: Session, user_id: int) -> models.User | None:
	return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_external_id(db: Session, user_id: int) -> models.User | None:
	return db.query(models.User).filter(models.User.external_id == user_id).first()



def create_plan(
	db: Session, user: models.User, plan_payload: dict, tip: str | None
) -> models.Plan:
	plan = models.Plan(
		user_id=user.id,
		original_plan=json.dumps(plan_payload),
		updated_plan=None,
		tip=tip,
		created_at=datetime.utcnow(),
		updated_at=datetime.utcnow(),
	)
	db.add(plan)
	db.commit()
	db.refresh(plan)
	return plan


def update_plan(
	db: Session, plan: models.Plan, plan_payload: dict, tip: str | None
) -> models.Plan:
	plan.updated_plan = json.dumps(plan_payload)
	plan.tip = tip
	plan.updated_at = datetime.utcnow()
	db.commit()
	db.refresh(plan)
	return plan


def get_plan(db: Session, plan_id: int) -> models.Plan | None:
	return db.query(models.Plan).filter(models.Plan.id == plan_id).first()


def get_latest_plan_for_user(db: Session, user_id: int) -> models.Plan | None:
	return (
		db.query(models.Plan)
		.filter(models.Plan.user_id == user_id)
		.order_by(models.Plan.created_at.desc())
		.first()
	)


def get_all_users(db: Session) -> list[models.User]:
	return db.query(models.User).order_by(models.User.created_at.desc()).all()


def create_feedback(
	db: Session, plan: models.Plan, feedback_text: str
) -> models.Feedback:
	feedback = models.Feedback(plan_id=plan.id, comment=feedback_text)
	db.add(feedback)
	db.commit()
	db.refresh(feedback)
	return feedback
