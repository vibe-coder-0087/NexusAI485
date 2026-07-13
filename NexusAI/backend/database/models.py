"""
SQLAlchemy models for NexusAI.

Kept intentionally simple for the MVP: every agent's data hangs off a
Conversation/Message pair or its own small table, all scoped to a User.
"""
from datetime import datetime
from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversations = db.relationship("Conversation", backref="user", lazy=True)
    study_plans = db.relationship("StudyPlan", backref="user", lazy=True)
    resume_reviews = db.relationship("ResumeReview", backref="user", lazy=True)
    pdf_documents = db.relationship("PDFDocument", backref="user", lazy=True)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "name": self.name}


class Conversation(db.Model):
    """A conversation thread with one of the AI agents (chat, coding, or pdf_chat)."""
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    agent_type = db.Column(db.String(50), nullable=False)  # 'chat' | 'coding' | 'pdf_chat'
    title = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship("Message", backref="conversation", lazy=True,
                                order_by="Message.created_at",
                                cascade="all, delete-orphan")

    def to_dict(self, include_messages=False):
        data = {
            "id": self.id,
            "agent_type": self.agent_type,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
        }
        if include_messages:
            data["messages"] = [m.to_dict() for m in self.messages]
        return data


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' | 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }


class StudyPlan(db.Model):
    __tablename__ = "study_plans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    goal = db.Column(db.Text, nullable=False)
    plan_json = db.Column(db.Text, nullable=False)  # JSON-encoded plan
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "goal": self.goal,
            "plan": json.loads(self.plan_json),
            "created_at": self.created_at.isoformat(),
        }


class ResumeReview(db.Model):
    __tablename__ = "resume_reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "feedback": self.feedback,
            "created_at": self.created_at.isoformat(),
        }


class PDFDocument(db.Model):
    __tablename__ = "pdf_documents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "conversation_id": self.conversation_id,
            "created_at": self.created_at.isoformat(),
        }
