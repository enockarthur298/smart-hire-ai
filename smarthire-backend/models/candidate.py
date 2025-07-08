from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    cv_file_path = db.Column(db.String(200))
    total_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ResumeScore(db.Model):
    __tablename__ = 'resume_score'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    skills_score = db.Column(db.Integer)
    exp_score = db.Column(db.Integer)
    edu_score = db.Column(db.Integer)
    raw_json = db.Column(db.Text)  # Store resume as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


