from flask import Flask, request, render_template
from transformers import pipeline
import fitz  # PyMuPDF
import os

app = Flask(__name__)
generator = pipeline("text-generation", model="distilgpt2")

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

@app.route('/', methods=['GET', 'POST'])
def index():
    critique = None
    if request.method == 'POST':
        file = request.files['resume']
        if file and file.filename.endswith('.pdf'):
            resume_text = extract_text(file)
            prompt = (
                "You are a professional resume reviewer.\n"
                "Please read the following resume and return a short critique in three parts:\n"
                "1. Strengths\n2. Weaknesses\n3. Suggestions for improvement.\n\n"
                "Only generate one response and do not repeat yourself.\n"
                "Resume:\n"
                f"{resume_text}"
            )
            result = generator(prompt, max_length=500, do_sample=True)
            critique = result[0]['generated_text']
    return render_template('index.html', critique=critique)
    
if __name__ == '__main__':
    app.run(port=3001)