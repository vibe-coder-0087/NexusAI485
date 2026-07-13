"""HTTP endpoints for the Coding Agent."""
from flask import Blueprint, request, jsonify
from middleware.validator import require_json_fields
from services.coding_service import handle_coding_request

coding_bp = Blueprint("coding", __name__, url_prefix="/api/coding")


@coding_bp.route("/message", methods=["POST"])
@require_json_fields("message")
def send_message():
    data = request.get_json()
    reply, conversation_id = handle_coding_request(
        prompt_text=data["message"],
        code_snippet=data.get("code"),
        language=data.get("language"),
        conversation_id=data.get("conversation_id"),
        user_id=data.get("user_id"),
        provider=data.get("provider"),
    )
    return jsonify({"reply": reply, "conversation_id": conversation_id})
