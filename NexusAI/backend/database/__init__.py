"""
Database package for NexusAI.
Exposes a single SQLAlchemy() instance (`db`) that the rest of the app imports,
and an `init_db(app)` helper that binds it to the Flask app and creates tables.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Bind SQLAlchemy to the Flask app and create tables if they don't exist."""
    db.init_app(app)
    with app.app_context():
        # Import models here so they're registered on the metadata before create_all()
        from database import models  # noqa: F401
        db.create_all()
