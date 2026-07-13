"""HTTP endpoints for the general Chat Agent."""
from flask import Blueprint, request, jsonify
from middleware.validator import require_json_fields
from services.chat_service import handle_chat_message, get_conversation_history, list_conversations

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


@chat_bp.route("/message", methods=["POST"])
@require_json_fields("message")
def send_message():
    data = request.get_json()
    reply, conversation_id = handle_chat_message(
        message_text=data["message"],
        conversation_id=data.get("conversation_id"),
        user_id=data.get("user_id"),
        provider=data.get("provider"),
    )
    return jsonify({"reply": reply, "conversation_id": conversation_id})


@chat_bp.route("/conversations", methods=["GET"])
def conversations():
    user_id = request.args.get("user_id", type=int)
    return jsonify(list_conversations(agent_type="chat", user_id=user_id))


@chat_bp.route("/conversations/<int:conversation_id>", methods=["GET"])
def conversation_detail(conversation_id):
    return jsonify(get_conversation_history(conversation_id))
