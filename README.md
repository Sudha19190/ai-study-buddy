# AI Study Buddy — Instant Lesson & Quiz Generator

A small Flask web app that turns any topic into a short lesson summary and a
5-question multiple-choice quiz, using Google's Gemini API. Built as a quick
demonstration of AI-assisted curriculum content generation.

## How it works
1. You type a topic (e.g. "Photosynthesis") and pick a grade level.
2. The Flask backend sends a structured prompt to the Gemini API asking for
   a lesson summary + quiz in JSON format.
3. The frontend renders the lesson as bullet points and the quiz as an
   interactive multiple-choice widget — click an option to see if you're
   right, with an explanation.

## Tech stack
Python, Flask, HTML, CSS, JavaScript, Gemini API (REST)

## Setup
1. Install dependencies:
   ```
   pip install flask requests
   ```
2. Get a **free** Gemini API key: https://aistudio.google.com/app/apikey
3. Set it as an environment variable:
   - Windows (PowerShell): `$env:GEMINI_API_KEY="your_key_here"`
   - Mac/Linux: `export GEMINI_API_KEY="your_key_here"`
4. Run the app:
   ```
   python app.py
   ```
5. Open http://127.0.0.1:5000 in your browser.

## Possible extensions (good "next steps" to mention in an interview)
- Save generated lessons/quizzes to a MySQL database (you already know SQL —
  this is a natural upgrade) so students can revisit past topics.
- Add a "difficulty" selector to further tailor content.
- Export a lesson + quiz as a downloadable PDF handout.
- Track quiz scores over multiple attempts.

## Why this project
Built to directly demonstrate the core responsibilities of an AI Education
Content & Curriculum Intern role: researching a topic, generating structured
learning content, and packaging it into an assessment — using AI tools as
the actual content-generation engine, not just as a research aid.
