"""
Business logic for the Resume Agent.
Accepts resume text (already extracted by the route layer) and returns
structured, actionable feedback.
"""
from database import db
from database.models import ResumeReview
from prompts.system_prompts import RESUME_AGENT_PROMPT
from services.ai_service import generate_response


def analyze_resume(resume_text, filename, target_role=None, user_id=None, provider=None):
    user_message = f"Here is the resume text:\n\n{resume_text}"
    if target_role:
        user_message += f"\n\nThe candidate is targeting this type of role: {target_role}"

    messages = [{"role": "user", "content": user_message}]
    feedback = generate_response(RESUME_AGENT_PROMPT, messages, provider=provider, max_tokens=1800)

    record = ResumeReview(user_id=user_id, filename=filename, feedback=feedback)
    db.session.add(record)
    db.session.commit()

    return record.to_dict()


def list_resume_reviews(user_id=None):
    query = ResumeReview.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    reviews = query.order_by(ResumeReview.created_at.desc()).all()
    return [r.to_dict() for r in reviews]
