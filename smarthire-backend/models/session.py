from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from .candidate import db  # reuse the existing db instance

class InterviewSession(db.Model):
    __tablename__ = 'interview_sessions'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    total_score = db.Column(db.Float)
    total_time = db.Column(db.Integer)  # in seconds
    question_count = db.Column(db.Integer)
    total_questions = db.Column(db.Integer, default=0)
    total_duration = db.Column(db.Integer, default=0)

class ChatLog(db.Model):
    __tablename__ = 'chat_log'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("interview_sessions.id")) 
    question = db.Column(db.Text)  # ✅ ADD THIS LINE
    answer = db.Column(db.Text)
    score = db.Column(db.Float)

class InterviewQuestion(db.Model):
    __tablename__ = 'interview_questions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("interview_sessions.id"))
    question = db.Column(db.Text)
    asked = db.Column(db.Boolean, default=False)
