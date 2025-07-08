from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from models.candidate import db  # reuse existing db instance
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Interview(db.Model):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    interview_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    status = db.Column(db.String(20), default='Scheduled')

    token = db.Column(db.String(64), unique=True, nullable=False)  # ✅ Add this

    candidate = db.relationship('Candidate', backref='interviews')
