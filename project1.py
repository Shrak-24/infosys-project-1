from flask import Flask, render_template, request
import os
import re
from docx import Document
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- TEXT EXTRACTION FUNCTION ----------------

def extract_text(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text

    return ""

# ---------------- TEXT CLEANING FUNCTION ----------------

def clean_text(text):
    text = text.lower()                        # lowercase
    text = re.sub(r'\n', ' ', text)            # remove new lines
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # remove special characters
    text = re.sub(r'\s+', ' ', text)           # remove extra spaces
    return text

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    resume = request.files['resume']
    jobdesc = request.files['jobdesc']

    allowed = ['pdf', 'docx', 'txt']

    # Validate file format
    if resume.filename.split('.')[-1].lower() not in allowed:
        return "Invalid Resume Format"

    if jobdesc.filename.split('.')[-1].lower() not in allowed:
        return "Invalid Job Description Format"

    # Save files
    resume_path = os.path.join(UPLOAD_FOLDER, resume.filename)
    jobdesc_path = os.path.join(UPLOAD_FOLDER, jobdesc.filename)

    resume.save(resume_path)
    jobdesc.save(jobdesc_path)

    # Extract text
    resume_text = extract_text(resume_path)
    jobdesc_text = extract_text(jobdesc_path)

    # Clean text
    clean_resume = clean_text(resume_text)
    clean_jobdesc = clean_text(jobdesc_text)

    # For now, print first 500 characters in terminal
    print("\n------ CLEAN RESUME TEXT ------\n")
    print(clean_resume[:500])

    print("\n------ CLEAN JOB DESCRIPTION TEXT ------\n")
    print(clean_jobdesc[:500])

    return render_template("success.html")

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run()