from flask import Flask, request, jsonify
from resume_parser import extract_text_from_pdf, extract_text_from_docx
import os

app = Flask(__name__)

# Create an uploads folder
UPLOAD_FOLDER = "../data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return {"message": "AI Resume Tailor API is running ✅"}

@app.route("/upload", methods=["POST"])
def upload_resume():
    # Check if file is in the request
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    
    file = request.files['resume']
    job_description = request.form.get('job_description', '')

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save file temporarily
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract text from PDF or DOCX
    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({
        "resume_text": resume_text[:500],  # only first 500 chars for now
        "job_description_received": job_description
    })

if __name__ == "__main__":
    app.run(debug=True)
