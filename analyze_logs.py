import requests
import json
import os

# Read logs
try:
    with open("pipeline.log", "r") as f:
        logs = f.read()
except Exception as e:
    logs = f"No logs found: {e}"

logs = logs[:4000]

# Read which failure scenario
failure_type = os.environ.get("FAILURE_TYPE", "unknown")

prompt = f"""
You are a DevOps expert.
Analyze this Azure DevOps pipeline failure log.
The failure type is: {failure_type}

Respond ONLY with raw JSON, no markdown, no extra text:
{{
  "failure_type": "",
  "error_type": "",
  "root_cause": "",
  "fix_suggestion": ""
}}

Log:
{logs}
"""

print(f"Calling Ollama for failure: {failure_type}")

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    result = response.json()
    raw = result["response"]

    try:
        parsed = json.loads(raw)
        print("===== AI RCA RESULT =====")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print("===== RAW RESPONSE =====")
        print(raw)

except Exception as e:
    print("Ollama call failed:", str(e))