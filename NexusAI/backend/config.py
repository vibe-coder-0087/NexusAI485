"""
Loads environment variables and centralizes app-wide settings.
Copy .env.example to .env and fill in values before running.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _split_origins(raw):
    if not raw:
        return ["http://localhost:5173"]
    return [o.strip() for o in raw.split(",") if o.strip()]


class Config:
    # --- Core ---
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    PORT = int(os.getenv("PORT", "5000"))

    # --- Database ---
    # Defaults to a local SQLite file. On Render, set DATABASE_URL to the
    # Postgres connection string provided by the managed database.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///nexus_ai.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- CORS ---
    # Comma-separated list, e.g. "https://your-app.vercel.app,http://localhost:5173"
    CORS_ORIGINS = _split_origins(os.getenv("CORS_ORIGINS"))

    # --- AI provider ---
    # "openai", "anthropic", or a request-level override of either
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")

    # --- Uploads ---
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.dirname(__file__), "uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024  # default 10MB
    ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx", "txt"}
    ALLOWED_PDF_EXTENSIONS = {"pdf"}
