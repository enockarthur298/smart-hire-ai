# File: routes/candidate.py

from flask import Blueprint, jsonify
from models.candidate import Candidate

candidate_bp = Blueprint('candidate_bp', __name__)

@candidate_bp.route('/recent_candidates', methods=['GET'])
def get_recent_candidates():
    candidates = Candidate.query.order_by(Candidate.created_at.desc()).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "total_score": c.total_score
        } for c in candidates
    ])
