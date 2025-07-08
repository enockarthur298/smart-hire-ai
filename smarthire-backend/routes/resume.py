from flask import Blueprint, request, jsonify
from models.candidate import Candidate, ResumeScore, db
from scorer import calculate_score
from llama_parser import parse_resume_with_llama
import fitz, json, os

resume_bp = Blueprint('resume_bp', __name__)

@resume_bp.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    filename = file.filename.lower()

    # ✅ Ensure the uploads folder exists
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    # ✅ Save file inside the uploads folder
    upload_path = os.path.join(upload_folder, filename)
    file.save(upload_path)

    # ✅ Read text from PDF
    if filename.endswith(".pdf"):
        doc = fitz.open(upload_path)
        text = "".join([page.get_text() for page in doc])
    else:
        text = file.read().decode('utf-8')

    if not text.strip():
        return jsonify({"error": "Resume is empty"}), 400

    # ✅ Parse & Score Resume
    parsed_data = parse_resume_with_llama(text)
    score = calculate_score(parsed_data)

    # ✅ Save Candidate Info
    new_candidate = Candidate(
        name=parsed_data["name"],
        email=parsed_data["email"],
        cv_file_path=upload_path,
        total_score=score
    )
    db.session.add(new_candidate)
    db.session.commit()

    # ✅ Save Resume Scoring Breakdown
    resume_score = ResumeScore(
        candidate_id=new_candidate.id,
        skills_score=40,
        exp_score=30,
        edu_score=10,
        raw_json=json.dumps(parsed_data)
    )
    db.session.add(resume_score)
    db.session.commit()

    return jsonify({"parsed": parsed_data, "score": score})

