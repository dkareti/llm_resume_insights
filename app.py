from flask import Flask, request, render_template
from transformers import pipeline
import fitz  # PyMuPDF
import os

app = Flask(__name__)
generator = pipeline("text-generation", model="distilgpt2")

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def extract_keywords(resume_text):
    lines = resume_text.split("\n")
    skills = []
    edu = []
    for line in lines:
        if any(word in line for word in ["Python", "Flask", "NLP", "C++", "Java", "ML"]):
            skills.append(line.strip())
        if "University" in line or "College" in line:
            edu.append(line.strip())
    return ", ".join(set(skills)), ", ".join(set(edu))

@app.route("/", methods=["GET", "POST"])
def index():
    tagline = None
    if request.method == "POST":
        file = request.files["resume"]
        if file and file.filename.endswith(".pdf"):
            resume_text = extract_text(file)
            skills, edu = extract_keywords(resume_text)
            prompt = f"Generate a catchy professional tagline for someone with skills in {skills}, with a background in {edu}."
            result = generator(prompt, max_length=50, do_sample=True, temperature=0.8)
            tagline = result[0]["generated_text"]
    return render_template("index.html", tagline=tagline)
    
if __name__ == '__main__':
    app.run(port=3001)