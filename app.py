from flask import Flask, request, render_template
from transformers import pipeline
import fitz  # PyMuPDF
import os

app = Flask(__name__)
generator = pipeline("text-generation", model="distilgpt2")

@app.route("/", methods=["GET", "POST"])
def index():
    tagline = None
    if request.method == "POST":
        job_title = request.form["job_title"]
        skills = request.form["skills"]
        education = request.form["education"]

        prompt = (
            "Job Title: Software Engineer\n"
            "Skills: Python, AI, Prompt Engineering\n"
            "Education: M.Eng in Computer Engineering at Dartmouth College\n"
            "Tagline:"
        )

        result = generator(prompt, max_length=60, do_sample=True, temperature=0.9)
        tagline = result[0]["generated_text"]
    return render_template("index.html", tagline=tagline)
    
if __name__ == '__main__':
    app.run(port=3001)