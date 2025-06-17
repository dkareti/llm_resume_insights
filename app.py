from flask import Flask, request, render_template
from transformers import pipeline
import os

app = Flask(__name__)
generator = None  # define globally but not load

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

        try:
            result = get_generator()(prompt, max_length=40, temperature=0.9)
            tagline = result[0]["generated_text"].strip()
        except Exception as e:
            tagline = f"Error: {str(e)}"

    return render_template("index.html", tagline=tagline)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)