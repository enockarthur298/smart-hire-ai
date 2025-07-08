from flask import Blueprint, request, jsonify
from models.candidate import db, Candidate
from models.interview import Interview
from datetime import datetime, timedelta, time as time_obj
from flask_mail import Message
from extensions import mail
import uuid

interview_bp = Blueprint('interview_bp', __name__)




# Interview constants
MAX_INTERVIEWS_PER_DAY = 10
INTERVIEW_DURATION = 30  # in minutes
GAP_DURATION = 20  # in minutes
START_TIME = time_obj(hour=8, minute=0)
END_TIME = time_obj(hour=20, minute=0)

# Utility to find next available slot
def get_next_slot():
    current_date = datetime.now().date() + timedelta(days=2)

    while True:
        # Skip weekends
        if current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            current_date += timedelta(days=1)
            continue

        # Get all interviews for that date
        existing = Interview.query.filter_by(interview_date=current_date).order_by(Interview.start_time).all()

        if len(existing) < MAX_INTERVIEWS_PER_DAY:
            if not existing:
                start = datetime.combine(current_date, START_TIME)
            else:
                last = existing[-1]
                last_end = datetime.combine(current_date, last.end_time)
                start = last_end + timedelta(minutes=GAP_DURATION)

            end = start + timedelta(minutes=INTERVIEW_DURATION)

            # Check if end time is still within working hours
            if end.time() <= END_TIME:
                return current_date, start.time(), end.time()

        # If full or invalid, try next day
        current_date += timedelta(days=1)


@interview_bp.route('/send_invitation', methods=['POST'])
def send_invitation():
    data = request.get_json()

    # ✅ Check candidate_id
    if 'candidate_id' not in data:
        return jsonify({"error": "Missing candidate_id"}), 400

    # ✅ Get candidate
    candidate = Candidate.query.get(data['candidate_id'])
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    try:
        # ✅ Use provided date/time if available, else auto-generate
        if all(k in data for k in ['date', 'start_time', 'end_time']):
            interview_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
            start_time = datetime.strptime(data['start_time'], "%H:%M").time()
            end_time = datetime.strptime(data['end_time'], "%H:%M").time()
        else:
            interview_date, start_time, end_time = get_next_slot()

        # ✅ Generate secure token
        token = str(uuid.uuid4())

        # ✅ Save interview
        interview = Interview(
            candidate_id=candidate.id,
            interview_date=interview_date,
            start_time=start_time,
            end_time=end_time,
            status="Scheduled",
            token=token
        )
        db.session.add(interview)
        db.session.commit()

        # ✅ Send email
        interview_link = f"http://localhost:3000/interview/{token}"
        msg = Message(
            subject="You're Invited: Interview with SmartHireAI 🎯",
            sender="sami325532@gmail.com",
            recipients=[candidate.email],
        )
        msg.body = f"""
Dear {candidate.name},

You're invited to your personalized AI interview.

Click the link below to begin:
👉 {interview_link}

Make sure you're ready – the interview starts when you open the link.

Regards,
SmartHireAI Team
"""

        mail.send(msg)

        return jsonify({
            "message": "Interview scheduled and email sent successfully.",
            "token": token
        }), 201

    except ValueError as e:
        return jsonify({"error": f"Invalid date/time format: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500
