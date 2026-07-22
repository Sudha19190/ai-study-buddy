import os
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set in this terminal session.")
    print("Run: set GEMINI_API_KEY=your_key_here")
    exit(1)

resp = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    headers={"x-goog-api-key": GEMINI_API_KEY},
    timeout=30,
)

print("Status code:", resp.status_code)
print()

if resp.status_code != 200:
    print("Error response:")
    print(resp.text)
else:
    data = resp.json()
    print("Models available to this key:")
    for m in data.get("models", []):
        name = m.get("name", "")
        methods = m.get("supportedGenerationMethods", [])
        if "generateContent" in methods:
            print(" -", name)