from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	external_id = Column(Integer, nullable=False, index=True)
	name = Column(String(100), nullable=False)
	age = Column(Integer, nullable=False)
	weight = Column(Integer, nullable=False)
	goal = Column(String(50), nullable=False)
	intensity = Column(String(20), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

	plans = relationship("Plan", back_populates="user", cascade="all, delete-orphan")


class Plan(Base):
	__tablename__ = "plans"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	original_plan = Column(Text, nullable=False)
	updated_plan = Column(Text, nullable=True)
	tip = Column(Text, nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

	user = relationship("User", back_populates="plans")
	feedback_items = relationship(
		"Feedback",
		back_populates="plan",
		cascade="all, delete-orphan",
	)


class Feedback(Base):
	__tablename__ = "feedback"

	id = Column(Integer, primary_key=True, index=True)
	plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
	comment = Column(Text, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

	plan = relationship("Plan", back_populates="feedback_items")
