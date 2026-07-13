"""
Business logic for the PDF Chat Agent.
Stores extracted PDF text once, then answers grounded questions against it
within a Conversation thread (agent_type='pdf_chat').
"""
from database import db
from database.models import Conversation, Message, PDFDocument
from prompts.system_prompts import PDF_CHAT_AGENT_PROMPT
from services.ai_service import generate_response
from middleware.error_handler import AppError

HISTORY_LIMIT = 12


def store_pdf(filename, extracted_text, user_id=None):
    conv = Conversation(agent_type="pdf_chat", user_id=user_id, title=filename)
    db.session.add(conv)
    db.session.flush()  # get conv.id before commit

    doc = PDFDocument(
        user_id=user_id,
        filename=filename,
        extracted_text=extracted_text,
        conversation_id=conv.id,
    )
    db.session.add(doc)
    db.session.commit()

    return doc, conv


def ask_pdf_question(conversation_id, question, provider=None):
    conv = Conversation.query.get(conversation_id)
    if not conv or conv.agent_type != "pdf_chat":
        raise AppError("PDF conversation not found", 404)

    doc = PDFDocument.query.filter_by(conversation_id=conversation_id).first()
    if not doc:
        raise AppError("No PDF associated with this conversation", 404)

    user_msg = Message(conversation_id=conv.id, role="user", content=question)
    db.session.add(user_msg)
    db.session.commit()

    recent = conv.messages[-HISTORY_LIMIT:]
    history = [{"role": m.role, "content": m.content} for m in recent]

    # Ground the request in the document text on every call (documents can be
    # long, so we keep this separate from the rolling chat history above).
    grounded_system_prompt = (
        f"{PDF_CHAT_AGENT_PROMPT}\n\n--- DOCUMENT: {doc.filename} ---\n{doc.extracted_text}\n--- END DOCUMENT ---"
    )

    reply_text = generate_response(grounded_system_prompt, history, provider=provider, max_tokens=1200)

    assistant_msg = Message(conversation_id=conv.id, role="assistant", content=reply_text)
    db.session.add(assistant_msg)
    db.session.commit()

    return reply_text
