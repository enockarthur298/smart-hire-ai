from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from llama_parser import parse_resume_with_llama
from scorer import calculate_score
import fitz  

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
    else:
        text = file.read().decode('utf-8')  # For .txt only
        
    if not text.strip():
      return jsonify({"error": "Resume file is empty or unreadable."}), 400
    
    print("here is the text of cv",text)
    parsed_data = parse_resume_with_llama(text)
    score = calculate_score(parsed_data)

    return jsonify({
        "parsed": parsed_data,
        "score": score
    })

# 👇 This part is required to start the server!
if __name__ == '__main__':
    app.run(debug=True)
