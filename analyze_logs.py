import os
import requests
import json

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

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

print("Status Code:", response.status_code)
print("Raw Response:", response.text)

# Handle response safely
if response.status_code == 200:
    try:
        result = response.json()
        print("===== AI RCA RESULT =====")
        print(json.dumps(result, indent=2))
    except:
        print("JSON parsing failed")
else:
    print("API call failed")

    fallback = {
        "error_type": "Build Failure",
        "root_cause": "HuggingFace API error",
        "fix_suggestion": "Check API endpoint or token"
    }

    print(json.dumps(fallback, indent=2))