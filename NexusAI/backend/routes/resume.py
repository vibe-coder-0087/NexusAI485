"""
HTTP endpoints for the Resume Agent.
Accepts an uploaded resume file (.pdf, .docx, or .txt), extracts its text,
and returns AI-generated feedback.
"""
import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from middleware.error_handler import AppError
from middleware.validator import require_file
from services.resume_service import analyze_resume, list_resume_reviews
from utils.pdf_parser import extract_text as extract_pdf_text
from utils.logger import get_logger

resume_bp = Blueprint("resume", __name__, url_prefix="/api/resume")
logger = get_logger(__name__)


def _allowed(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_RESUME_EXTENSIONS"], ext


def _extract_text(saved_path, ext):
    if ext == "pdf":
        return extract_pdf_text(saved_path)
    if ext == "txt":
        with open(saved_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if ext == "docx":
        try:
            import docx
        except ImportError as exc:
            raise AppError("python-docx package not installed on the server", 500) from exc
        document = docx.Document(saved_path)
        return "\n".join(p.text for p in document.paragraphs if p.text.strip())
    raise AppError(f"Unsupported file type: .{ext}", 400)


@resume_bp.route("/analyze", methods=["POST"])
@require_file("resume")
def analyze():
    file = request.files["resume"]
    is_allowed, ext = _allowed(file.filename)
    if not is_allowed:
        raise AppError("Please upload a .pdf, .docx, or .txt resume", 400)

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    saved_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file.save(saved_path)

    try:
        resume_text = _extract_text(saved_path, ext)
        if not resume_text.strip():
            raise AppError("Couldn't find readable text in this file", 400)

        target_role = request.form.get("target_role")
        user_id = request.form.get("user_id", type=int)
        provider = request.form.get("provider")

        result = analyze_resume(
            resume_text=resume_text,
            filename=filename,
            target_role=target_role,
            user_id=user_id,
            provider=provider,
        )
        return jsonify(result)
    finally:
        # Uploaded resumes may contain sensitive personal data - don't keep the raw file
        if os.path.exists(saved_path):
            os.remove(saved_path)


@resume_bp.route("/reviews", methods=["GET"])
def reviews():
    user_id = request.args.get("user_id", type=int)
    return jsonify(list_resume_reviews(user_id=user_id))
