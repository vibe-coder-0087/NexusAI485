"""
Business logic for the Study Agent.
Turns a goal + constraints into a structured, storable study plan.
"""
import json
import re
from database import db
from database.models import StudyPlan
from prompts.system_prompts import STUDY_AGENT_PROMPT
from services.ai_service import generate_response
from middleware.error_handler import AppError


def _extract_json(text):
    """The model is instructed to return raw JSON, but strip code fences defensively."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AppError("The AI returned an unexpected format for the study plan. Please try again.", 502) from exc


def generate_study_plan(goal, subjects=None, hours_per_day=None, deadline=None,
                         user_id=None, provider=None):
    prompt_parts = [f"Goal: {goal}"]
    if subjects:
        prompt_parts.append(f"Subjects/topics: {subjects}")
    if hours_per_day:
        prompt_parts.append(f"Available study time: {hours_per_day} hours/day")
    if deadline:
        prompt_parts.append(f"Deadline: {deadline}")

    user_message = "\n".join(prompt_parts)
    messages = [{"role": "user", "content": user_message}]

    raw_response = generate_response(STUDY_AGENT_PROMPT, messages, provider=provider, max_tokens=1500)
    plan_dict = _extract_json(raw_response)

    record = StudyPlan(user_id=user_id, goal=goal, plan_json=json.dumps(plan_dict))
    db.session.add(record)
    db.session.commit()

    return record.to_dict()


def list_study_plans(user_id=None):
    query = StudyPlan.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    plans = query.order_by(StudyPlan.created_at.desc()).all()
    return [p.to_dict() for p in plans]


def get_study_plan(plan_id):
    plan = StudyPlan.query.get(plan_id)
    if not plan:
        raise AppError("Study plan not found", 404)
    return plan.to_dict()
