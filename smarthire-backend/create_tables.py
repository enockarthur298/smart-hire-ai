from app import app
from models.candidate import db
from models.interview import Interview

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
