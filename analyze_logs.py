import os
import requests
import json

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": "Bearer " + os.getenv("HF_TOKEN")
}

# Read logs
try:
    with open("pipeline.log", "r") as f:
        logs = f.read()
except:
    logs = "No logs found"

logs = logs[:2000]

prompt = f"""
You are a DevOps expert.

Analyze this Azure DevOps pipeline failure log.

Provide output strictly in JSON:
{{
  "error_type": "",
  "root_cause": "",
  "fix_suggestion": ""
}}

Log:
{logs}
"""

print("Calling HuggingFace API...")

response = requests.post(
    API_URL,
    headers=headers,
    json={"inputs": prompt}
)

print("Raw response:")
print(response.text)   # 🔥 DEBUG (IMPORTANT)

try:
    result = response.json()

    print("===== AI RCA RESULT =====")
    print(json.dumps(result, indent=2))

except Exception as e:
    print("JSON parsing failed. Using fallback.")

    # Fallback logic
    fallback = {
        "error_type": "Build Failure",
        "root_cause": "Unable to parse AI response",
        "fix_suggestion": "Check logs manually or retry API"
    }

    print(json.dumps(fallback, indent=2))