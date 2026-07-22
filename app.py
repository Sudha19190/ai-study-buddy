"""
AI Study Buddy — Instant Lesson & Quiz Generator
--------------------------------------------------
Takes a topic + grade level from the user, calls the Gemini API,
and returns a short lesson summary plus a 5-question multiple-choice quiz.

Run:
    1. pip install flask requests
    2. Get a free Gemini API key: https://aistudio.google.com/app/apikey
    3. set GEMINI_API_KEY=your_key_here   (Windows)
       export GEMINI_API_KEY=your_key_here  (Mac/Linux)
    4. python app.py
    5. Open http://127.0.0.1:5000
"""

import os
import json
import re
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
print(f"DEBUG: Key loaded, length = {len(GEMINI_API_KEY)}")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.6-flash:generateContent"
)


def build_prompt(topic: str, grade: str) -> str:
    """Builds a prompt that asks Gemini for a lesson + quiz in strict JSON,
    so the frontend can render it reliably."""
    return f"""
You are an AI curriculum assistant creating learning content for a {grade} student.

Topic: "{topic}"

Return ONLY valid JSON (no markdown, no code fences) in exactly this shape:
{{
  "lesson_summary": ["point 1", "point 2", "point 3", "point 4"],
  "quiz": [
    {{
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A",
      "explanation": "..."
    }}
  ]
}}

Rules:
- lesson_summary: 4 short, clear bullet points explaining the topic simply.
- quiz: exactly 5 multiple-choice questions testing the lesson_summary content.
- Keep language appropriate for a {grade} student.
- Do not include anything outside the JSON object.
"""


def call_gemini(prompt: str) -> dict:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "No GEMINI_API_KEY set. Get a free key at "
            "https://aistudio.google.com/app/apikey and set it as an "
            "environment variable before running the app."
        )

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(
        GEMINI_URL,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        },
        json=payload,
        timeout=30,
    )
    print("DEBUG status:", resp.status_code, flush=True)
    print("DEBUG body:", resp.text[:1000], flush=True)
    print("DEBUG status:", resp.status_code)
    print("DEBUG body:", resp.text[:1000])
    resp.raise_for_status()
    data = resp.json()

    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]

    # Strip stray markdown fences if the model adds them anyway
    cleaned = re.sub(r"^```json|^```|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    body = request.get_json(force=True)
    topic = (body.get("topic") or "").strip()
    grade = (body.get("grade") or "high school").strip()

    if not topic:
        return jsonify({"error": "Please enter a topic."}), 400

    try:
        prompt = build_prompt(topic, grade)
        result = call_gemini(prompt)
        return jsonify(result)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5050)
