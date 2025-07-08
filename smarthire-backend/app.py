from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from flask_migrate import Migrate
import logging

from extensions import mail
from models.candidate import db
from models import candidate, interview  # ✅ Make sure all models are imported
from routes.resume import resume_bp
from routes.interview import interview_bp
from routes.candidate import candidate_bp
from routes.chat import chat_bp

# Load env vars
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)

# Flask app
app = Flask(__name__)
CORS(app) 
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)   # ✅ This is key

# Register Blueprints
app.register_blueprint(resume_bp)
app.register_blueprint(interview_bp)
app.register_blueprint(candidate_bp)
app.register_blueprint(chat_bp, url_prefix="/interview_chat")


# No need for db.create_all() — Flask-Migrate handles this

# Start server
if __name__ == '__main__':
    app.run(debug=True)
