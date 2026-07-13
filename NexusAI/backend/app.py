"""
Main application entry point.
Creates the Flask app, wires up config/DB/CORS/error handling, and
registers every agent's route blueprint.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from database import init_db
from middleware.error_handler import register_error_handlers
from utils.logger import get_logger

from routes.chat import chat_bp
from routes.coding import coding_bp
from routes.study import study_bp
from routes.resume import resume_bp
from routes.pdf_chat import pdf_chat_bp

logger = get_logger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

    init_db(app)
    register_error_handlers(app)

    app.register_blueprint(chat_bp)
    app.register_blueprint(coding_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(pdf_chat_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "service": "NexusAI backend",
            "ai_provider": Config.AI_PROVIDER,
        })

    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"message": "NexusAI API is running. See /api/health."})

    logger.info("NexusAI backend initialized (AI_PROVIDER=%s)", Config.AI_PROVIDER)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
