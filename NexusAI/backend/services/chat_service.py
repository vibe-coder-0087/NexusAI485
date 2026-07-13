"""
Business logic for the general Chat Agent.
Builds conversation context, calls ai_service, and persists messages.
"""
from database import db
from database.models import Conversation, Message
from prompts.system_prompts import CHAT_AGENT_PROMPT
from services.ai_service import generate_response
from middleware.error_handler import AppError

HISTORY_LIMIT = 20  # most recent messages sent as context


def _get_or_create_conversation(conversation_id, user_id=None):
    if conversation_id:
        conv = Conversation.query.get(conversation_id)
        if not conv:
            raise AppError("Conversation not found", 404)
        return conv
    conv = Conversation(agent_type="chat", user_id=user_id, title="New chat")
    db.session.add(conv)
    db.session.commit()
    return conv


def handle_chat_message(message_text, conversation_id=None, user_id=None, provider=None):
    conv = _get_or_create_conversation(conversation_id, user_id)

    user_msg = Message(conversation_id=conv.id, role="user", content=message_text)
    db.session.add(user_msg)
    db.session.commit()

    recent = conv.messages[-HISTORY_LIMIT:]
    history = [{"role": m.role, "content": m.content} for m in recent]

    reply_text = generate_response(CHAT_AGENT_PROMPT, history, provider=provider)

    assistant_msg = Message(conversation_id=conv.id, role="assistant", content=reply_text)
    db.session.add(assistant_msg)

    if conv.title == "New chat":
        conv.title = message_text[:60]

    db.session.commit()

    return reply_text, conv.id


def get_conversation_history(conversation_id):
    conv = Conversation.query.get(conversation_id)
    if not conv:
        raise AppError("Conversation not found", 404)
    return conv.to_dict(include_messages=True)


def list_conversations(agent_type="chat", user_id=None):
    query = Conversation.query.filter_by(agent_type=agent_type)
    if user_id:
        query = query.filter_by(user_id=user_id)
    conversations = query.order_by(Conversation.created_at.desc()).all()
    return [c.to_dict() for c in conversations]
