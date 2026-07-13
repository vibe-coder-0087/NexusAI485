"""
Business logic for the Coding Agent.
Reuses the same Conversation/Message tables as chat, tagged agent_type='coding'.
"""
from database import db
from database.models import Conversation, Message
from prompts.system_prompts import CODING_AGENT_PROMPT
from services.ai_service import generate_response
from middleware.error_handler import AppError

HISTORY_LIMIT = 20


def _get_or_create_conversation(conversation_id, user_id=None):
    if conversation_id:
        conv = Conversation.query.get(conversation_id)
        if not conv:
            raise AppError("Conversation not found", 404)
        return conv
    conv = Conversation(agent_type="coding", user_id=user_id, title="New coding session")
    db.session.add(conv)
    db.session.commit()
    return conv


def handle_coding_request(prompt_text, code_snippet=None, language=None,
                           conversation_id=None, user_id=None, provider=None):
    conv = _get_or_create_conversation(conversation_id, user_id)

    composed = prompt_text
    if code_snippet:
        lang_tag = language or ""
        composed += f"\n\n```{lang_tag}\n{code_snippet}\n```"

    user_msg = Message(conversation_id=conv.id, role="user", content=composed)
    db.session.add(user_msg)
    db.session.commit()

    recent = conv.messages[-HISTORY_LIMIT:]
    history = [{"role": m.role, "content": m.content} for m in recent]

    reply_text = generate_response(CODING_AGENT_PROMPT, history, provider=provider, max_tokens=1600)

    assistant_msg = Message(conversation_id=conv.id, role="assistant", content=reply_text)
    db.session.add(assistant_msg)

    if conv.title == "New coding session":
        conv.title = prompt_text[:60]

    db.session.commit()

    return reply_text, conv.id
