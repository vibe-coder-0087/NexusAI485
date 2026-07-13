"""
HTTP endpoints for the PDF Chat Agent.
Upload a PDF once (creates a conversation), then ask repeated questions
against it.
"""
import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from middleware.error_handler import AppError
from middleware.validator import require_file, require_json_fields
from services.pdf_chat_service import store_pdf, ask_pdf_question
from utils.pdf_parser import extract_text

pdf_chat_bp = Blueprint("pdf_chat", __name__, url_prefix="/api/pdf-chat")


@pdf_chat_bp.route("/upload", methods=["POST"])
@require_file("file")
def upload():
    file = request.files["file"]
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in current_app.config["ALLOWED_PDF_EXTENSIONS"]:
        raise AppError("Please upload a .pdf file", 400)

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    saved_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file.save(saved_path)

    try:
        extracted_text = extract_text(saved_path)
        user_id = request.form.get("user_id", type=int)
        doc, conv = store_pdf(filename=filename, extracted_text=extracted_text, user_id=user_id)
        return jsonify({
            "conversation_id": conv.id,
            "filename": doc.filename,
            "message": "PDF uploaded. You can now ask questions about it.",
        })
    finally:
        if os.path.exists(saved_path):
            os.remove(saved_path)


@pdf_chat_bp.route("/ask", methods=["POST"])
@require_json_fields("conversation_id", "question")
def ask():
    data = request.get_json()
    reply = ask_pdf_question(
        conversation_id=data["conversation_id"],
        question=data["question"],
        provider=data.get("provider"),
    )
    return jsonify({"reply": reply, "conversation_id": data["conversation_id"]})
