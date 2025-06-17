# llm_resume_insights

This is a web app that allows the user to upload a pdf resume and 
the app returns an AI-generated tagline using Hugging Face's `distilgpt2`
model.
The llm generates a summary suitable for LinkedIn headlines, bios, or portfolio intros.


To run this:
`pip install -r requirements.txt`
`python3 app.py`


### File Structure
llm_resume_critic/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css



To get better performance use different models BUT more parameters needs more GPU power.
