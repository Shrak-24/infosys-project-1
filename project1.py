from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    resume = request.files['resume']
    jobdesc = request.files['jobdesc']

    allowed = ['pdf', 'docx', 'txt']

    if resume.filename.split('.')[-1] not in allowed:
        return "Invalid Resume Format"

    if jobdesc.filename.split('.')[-1] not in allowed:
        return "Invalid Job Description Format"

    resume.save(os.path.join(UPLOAD_FOLDER, resume.filename))
    jobdesc.save(os.path.join(UPLOAD_FOLDER, jobdesc.filename))

    return render_template("success.html")


if __name__ == "__main__":
    app.run()
