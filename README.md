# llm_resume_insights

This is a web app that allows the user to upload a pdf resume and 
the app returns an AI-generated critique using Hugging Face's `Mistral-7B-Instruct`
model.

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