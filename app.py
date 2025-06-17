from flask import Flask, request, render_template
from transformers import pipeline
import fitz  # PyMuPDF
import os

app = Flask(__name__)
generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct", max_length=1024)

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
            prompt = f"Critique the following resume:\n{resume_text}\n\nInclude strengths, weaknesses, and areas for improvement."
            result = generator(prompt, max_length=500, do_sample=True)
            critique = result[0]['generated_text']
    return render_template('index.html', critique=critique)
    
if __name__ == '__main__':
    app.run(port=3001)