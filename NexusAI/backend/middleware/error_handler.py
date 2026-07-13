"""
Centralized error handling for the Flask app.

Any route can `raise AppError("message", status_code=400)` and it will be
caught here and turned into a consistent JSON response, instead of every
route needing its own try/except.
"""
from flask import jsonify
from utils.logger import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Raise this anywhere in the app for a controlled, client-facing error."""

    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self):
        data = dict(self.payload)
        data["error"] = self.message
        return data


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(err):
        logger.warning("AppError: %s", err.message)
        response = jsonify(err.to_dict())
        response.status_code = err.status_code
        return response

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(413)
    def handle_413(err):
        return jsonify({"error": "File too large"}), 413

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        logger.exception("Unhandled exception")
        return jsonify({"error": "Internal server error"}), 500
