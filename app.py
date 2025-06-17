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
            f"Create a professional tagline for a {job_title} skilled in {skills}, "
            f"with a background in {education}."
        )

        result = generator(prompt, max_length=50, do_sample=True, temperature=0.8)
        tagline = result[0]["generated_text"]
    return render_template("index.html", tagline=tagline)
    
if __name__ == '__main__':
    app.run(port=3001)