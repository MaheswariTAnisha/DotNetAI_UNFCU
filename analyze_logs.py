import os
import requests
import json
import time

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}

# Read logs
try:
    with open("pipeline.log", "r") as f:
        logs = f.read()
except:
    logs = "No logs found"

logs = logs[:1500]

prompt = f"""
You are a DevOps expert.

Analyze this Azure DevOps pipeline failure log.

Return ONLY JSON:
{{
  "error_type": "",
  "root_cause": "",
  "fix_suggestion": ""
}}

Log:
{logs}
"""

print("Calling HuggingFace API...")

for i in range(2):  # retry once
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    if response.status_code == 200:
        try:
            result = response.json()

            print("===== AI RCA RESULT =====")
            print(json.dumps(result, indent=2))
            break
        except:
            print("JSON parsing failed")
            break

    elif "loading" in response.text.lower():
        print("Model loading... retrying in 10 sec")
        time.sleep(10)
    else:
        print("API call failed")
        break

# Fallback (always safe)
fallback = {
    "error_type": "Build Failure",
    "root_cause": "AI response unavailable",
    "fix_suggestion": "Check logs manually"
}

print("===== FALLBACK RESULT =====")
print(json.dumps(fallback, indent=2))