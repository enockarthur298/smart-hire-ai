# interview_chat.py

from flask import Blueprint, request, jsonify
from models.candidate import Candidate
from models.interview import Interview
from models.session import InterviewSession, ChatLog, db
from datetime import datetime, timedelta
import uuid
from groq import Groq  # assuming Groq SDK is installed and configured
import os

chat_bp = Blueprint('chat_bp', __name__)

# ✅ Setup Groq Client (You must set your Groq API key as an environment variable)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ Constants
INTERVIEW_DURATION_MIN = 30

# 🧠 Helper: Generate follow-up question

def generate_followup_question(chat_history):
    messages = [
        {"role": "system", "content": "You are an AI interviewer. Ask technical follow-up questions based on the candidate's answers."},
        *chat_history,
    ]
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content


# 🧠 Helper: Score the answer

def score_answer(answer):
    system_prompt = (
        "You are an interview evaluator. Give a score (0-10) to this answer based on depth, accuracy, and clarity."
        " Only return the score as a float number."
    )
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": answer},
        ]
    )
    score_text = response.choices[0].message.content
    try:
        return float(score_text.strip())
    except:
        return 0.0


# ✅ Start session endpoint (recommended before /chat)
@chat_bp.route("/start_session", methods=["POST"])
def start_session():
    token = request.json.get("token")
    interview = Interview.query.filter_by(token=token).first()
    if not interview:
        return jsonify({"error": "Invalid token"}), 404

    # Check if session already exists
    session = InterviewSession.query.filter_by(interview_id=interview.id).first()
    if not session:
        session = InterviewSession(interview_id=interview.id)
        db.session.add(session)
        db.session.commit()

    return jsonify({"message": "Session started", "session_id": session.id})


# ✅ Chat route
@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    token = data.get("token")
    user_message = data.get("message")

    if not token or not user_message:
        return jsonify({"error": "Missing token or message"}), 400

    # ✅ Load Interview and Session
    interview = Interview.query.filter_by(token=token).first()
    if not interview:
        return jsonify({"error": "Invalid token"}), 404

    session = InterviewSession.query.filter_by(interview_id=interview.id).first()
    if not session:
        return jsonify({"error": "Session not started"}), 400

    # ✅ Timer Enforcement
    now = datetime.utcnow()
    if session.started_at and (now - session.started_at > timedelta(minutes=INTERVIEW_DURATION_MIN)):
        session.ended_at = now
        session.is_completed = True
        db.session.commit()
        return jsonify({"error": "Interview time is over"}), 403

    # ✅ Log user message
    user_log = ChatLog(session_id=session.id, sender="user", message=user_message)
    db.session.add(user_log)

    # ✅ Prepare chat history
    previous_logs = ChatLog.query.filter_by(session_id=session.id).order_by(ChatLog.timestamp).all()
    chat_history = []
    for log in previous_logs:
        chat_history.append({"role": "user" if log.sender == "user" else "assistant", "content": log.message})
    chat_history.append({"role": "user", "content": user_message})

    # ✅ Generate bot reply
    reply = generate_followup_question(chat_history)

    # ✅ Score answer
    score = score_answer(user_message)

    # ✅ Save bot reply + score
    bot_log = ChatLog(session_id=session.id, sender="bot", message=reply, score=score)
    db.session.add(bot_log)

    db.session.commit()

    return jsonify({
        "reply": reply,
        "score": score
    })
