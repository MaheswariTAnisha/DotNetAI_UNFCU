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

# Limit size
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

try:
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    result = response.json()

    print("===== AI RCA RESULT =====")
    print(json.dumps(result, indent=2))

except Exception as e:
    print("AI Analysis Failed:", str(e))