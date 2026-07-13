"""HTTP endpoints for the Study Agent."""
from flask import Blueprint, request, jsonify
from middleware.validator import require_json_fields
from services.study_service import generate_study_plan, list_study_plans, get_study_plan

study_bp = Blueprint("study", __name__, url_prefix="/api/study")


@study_bp.route("/plan", methods=["POST"])
@require_json_fields("goal")
def create_plan():
    data = request.get_json()
    plan = generate_study_plan(
        goal=data["goal"],
        subjects=data.get("subjects"),
        hours_per_day=data.get("hours_per_day"),
        deadline=data.get("deadline"),
        user_id=data.get("user_id"),
        provider=data.get("provider"),
    )
    return jsonify(plan)


@study_bp.route("/plans", methods=["GET"])
def plans():
    user_id = request.args.get("user_id", type=int)
    return jsonify(list_study_plans(user_id=user_id))


@study_bp.route("/plans/<int:plan_id>", methods=["GET"])
def plan_detail(plan_id):
    return jsonify(get_study_plan(plan_id))
