from flask import Blueprint, request, jsonify,json
from models.session import InterviewSession, db
from models.candidate import Candidate
import uuid
from datetime import datetime
from models.session import InterviewSession, ChatLog
from datetime import datetime
from groq import Groq
import os
import re
from utils.interview_generator import generate_questions_from_resume
from models.session import InterviewSession, InterviewQuestion, ChatLog
from models.candidate import ResumeScore

chat_bp = Blueprint('chat_bp', __name__)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))



@chat_bp.route("/start_session", methods=["POST"])
def start_session():
    candidate_id = request.json.get("candidate_id")
    candidate = Candidate.query.get(candidate_id)
    resume_score = ResumeScore.query.filter_by(candidate_id=candidate_id).first()

    if not resume_score:
        return jsonify({"error": "Resume score not found"}), 404

    token = str(uuid.uuid4())
    session = InterviewSession(candidate_id=candidate_id, token=token)
    db.session.add(session)
    db.session.commit()

    questions_text = generate_questions_from_resume(json.loads(resume_score.raw_json))
    for q in questions_text.split("\n"):
        q = q.strip("1234567890). ").strip()
        if q:
            db.session.add(InterviewQuestion(session_id=session.id, question=q))

    db.session.commit()
    return jsonify({"message": "Session started", "token": token})

@chat_bp.route("/chat", methods=["POST"])
def chat():
    print("✅ Chat endpoint called")
    data = request.get_json()
    print("Received data:", data)
    token = data.get("token")
    message = data.get("message")
    print("Token:", token)
    print("Message:", message)

    session = InterviewSession.query.filter_by(token=token).first()
    print("Session found:", session)
    if not session:
        return jsonify({"error": "Invalid token"}), 404

    if session.is_completed:
        return jsonify({"error": "Session ended"}), 400

    # Check time
    elapsed = (datetime.utcnow() - session.started_at).total_seconds()
    if elapsed > 1800:
        session.is_completed = True
        session.total_duration = int(elapsed)
        db.session.commit()
        return jsonify({"error": "Session expired (30 mins)"})

    # Get next question
    question_obj = InterviewQuestion.query.filter_by(session_id=session.id, asked=False).first()
    if not question_obj:
        session.is_completed = True
        session.total_duration = int(elapsed)
        db.session.commit()
        return jsonify({"message": "Interview complete."})

    question_text = question_obj.question
    question_obj.asked = True
    db.session.commit() 

    # Scoring with Groq
    reply = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": f"You are scoring a candidate's answer to an interview question.\nQuestion: {question_text}"},
            {"role": "user", "content": f"Answer: {message}\n\nScore out of 10 with justification."}
        ]
    ).choices[0].message.content.strip()

    score = extract_score_from_reply(reply)

    # Save log
    log = ChatLog(
        session_id=session.id,
        question=question_text,
        answer=message,
        score=score
    )
    db.session.add(log)

    if session.total_questions is None:
        session.total_questions = 0
    if session.total_score is None:
        session.total_score = 0

    session.total_questions += 1
    session.total_score = ((session.total_score * (session.total_questions - 1)) + score) / session.total_questions

    db.session.commit()

    return jsonify({
        "question": question_text,
        "reply": reply,
        "score": score
    })

@chat_bp.route("/report/<token>", methods=["GET"])
def report(token):
    session = InterviewSession.query.filter_by(token=token).first()
    if not session:
        return jsonify({"error": "Invalid session token"}), 404

    logs = ChatLog.query.filter_by(session_id=session.id).all()
    return jsonify({
        "candidate_id": session.candidate_id,
        "completed": session.is_completed,
        "total_score": session.total_score,
        "total_questions": session.total_questions,
        "total_duration_sec": session.total_duration,
        "logs": [
            {"question": log.question, "answer": log.answer, "score": log.score}
            for log in logs
        ]
    })
    
    
def extract_score_from_reply(reply):
    match = re.search(r'(?i)(score[:\s]*)(\d+(\.\d+)?)', reply)
    if match:
        return float(match.group(2))
    return 6.0  # default score if not found
    