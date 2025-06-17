from flask import Flask, request, render_template
from transformers import pipeline
import torch
import os

# Optimize for Apple Silicon CPU usage
torch.set_num_threads(4)

app = Flask(__name__)

def get_generator():
    global generator
    if generator is None:
        generator = pipeline("text2text-generation", model="google/flan-t5-small")
    return generator

@app.route("/", methods=["GET", "POST"])
def index():
    tagline = None
    if request.method == "POST":
        job_title = request.form["job_title"]
        skills = request.form["skills"]
        degree = request.form["degree"]
        field = request.form["field"]

        prompt = (
            f"Write a one-sentence, third-person LinkedIn tagline for a {job_title} "
            f"who is skilled in {skills} and holds a {degree} in {field}."
        )

        gen = get_generator()
        result = gen(prompt, max_length=40, temperature=0.9)
        tagline = result[0]["generated_text"].strip()
    return render_template("index.html", tagline=tagline)

@app.route("/ping")
def ping():
    return "Flask is alive!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)