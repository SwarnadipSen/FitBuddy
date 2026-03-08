import json
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud
from . import gemini_flash_generator
from . import gemini_generator
from . import schemas
from . import updated_plan
from .database import get_db

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


def _load_plan_payload(plan) -> str:
    return plan.updated_plan or plan.original_plan


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/plans", response_model=schemas.PlanResponse)
def create_plan(plan_in: schemas.PlanRequest, db: Session = Depends(get_db)):
    user = crud.upsert_user(db, plan_in)
    plan_text = gemini_generator.generate_workout_gemini(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = gemini_flash_generator.generate_nutrition_tip_with_flash(user.goal)
    plan = crud.create_plan(db, user, plan_text, tip)
    return schemas.PlanResponse(
        id=plan.id,
        user_id=user.id,
        plan=plan_text,
        tip=tip,
    )


@router.post("/feedback", response_model=schemas.PlanResponse)
def submit_feedback(feedback_in: schemas.FeedbackRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_external_id(db, feedback_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    plan = crud.get_latest_plan_for_user(db, user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    current_plan_text = _load_plan_payload(plan)
    updated_plan_text = updated_plan.update_workout_plan(
        current_plan=current_plan_text,
        feedback=feedback_in.feedback,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = gemini_flash_generator.generate_nutrition_tip_with_flash(user.goal)
    updated = crud.update_plan(db, plan, updated_plan_text, tip)
    crud.create_feedback(db, updated, feedback_in.feedback)
    return schemas.PlanResponse(
        id=updated.id,
        user_id=user.id,
        plan=updated_plan_text,
        tip=tip,
    )


@router.get("/tips", response_model=schemas.TipResponse)
def get_tip(goal: schemas.GoalType):
    tip = gemini_flash_generator.generate_nutrition_tip_with_flash(goal)
    return schemas.TipResponse(goal=goal, tip=tip)


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_external_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/plans/{plan_id}", response_model=schemas.PlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = crud.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan_text = _load_plan_payload(plan)
    return schemas.PlanResponse(
        id=plan.id,
        user_id=plan.user_id,
        plan=plan_text,
        tip=plan.tip,
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    user_id: int = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    plan_in = schemas.PlanRequest(
        user_id=user_id,
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )
    user = crud.upsert_user(db, plan_in)
    plan_text = gemini_generator.generate_workout_gemini(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = gemini_flash_generator.generate_nutrition_tip_with_flash(user.goal)
    plan = crud.create_plan(db, user, plan_text, tip)
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "plan": plan_text,
            "tip": tip,
            "user_id": user.external_id,
            "plan_id": plan.id,
        },
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback_ui(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_external_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    plan = crud.get_latest_plan_for_user(db, user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    current_plan_text = _load_plan_payload(plan)
    updated_plan_text = updated_plan.update_workout_plan(
        current_plan=current_plan_text,
        feedback=feedback,
        goal=user.goal,
        intensity=user.intensity,
    )
    tip = gemini_flash_generator.generate_nutrition_tip_with_flash(user.goal)
    updated = crud.update_plan(db, plan, updated_plan_text, tip)
    crud.create_feedback(db, updated, feedback)
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "plan": updated_plan_text,
            "tip": tip,
            "user_id": user.external_id,
            "plan_id": updated.id,
        },
    )


@router.get("/ui/plan/{plan_id}", response_class=HTMLResponse)
def ui_plan(plan_id: int, request: Request, db: Session = Depends(get_db)):
    plan = crud.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan_payload = _load_plan_payload(plan)
    return templates.TemplateResponse(
        "plan.html",
        {
            "request": request,
            "plan": plan_payload,
            "tip": plan.tip,
            "plan_id": plan.id,
        },
    )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    user_data = []
    for user in users:
        plan = crud.get_latest_plan_for_user(db, user.id)
        original_plan = "N/A"
        updated_plan = "Not updated"
        if plan:
            original_plan = plan.original_plan
            updated_plan = plan.updated_plan or "Not updated"
        user_data.append(
            {
                "user_id": user.external_id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": original_plan,
                "updated_plan": updated_plan,
            }
        )
    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": user_data,
        },
    )
