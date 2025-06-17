from flask import Flask, request, render_template
from transformers import pipeline
import torch

# Optimize for Apple Silicon CPU usage
torch.set_num_threads(4)

app = Flask(__name__)

# Load the instruction-tuned model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

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

        result = generator(prompt, max_length=40, temperature=0.9)
        tagline = result[0]["generated_text"].strip()
    return render_template("index.html", tagline=tagline)

if __name__ == "__main__":
    app.run(port=3001)