import requests
import json

try:
    with open("pipeline.log", "r") as f:
        logs = f.read()
except Exception as e:
    logs = f"No logs found: {e}"

logs = logs[:4000]

prompt = f"""
You are a DevOps expert.
Analyze this Azure DevOps pipeline failure log.
Respond ONLY with raw JSON, no markdown, no extra text:
{{
  "error_type": "",
  "root_cause": "",
  "fix_suggestion": ""
}}

Log:
{logs}
"""

print("Calling Ollama (local)...")

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",   # make sure this matches: ollama list
            "prompt": prompt,
            "stream": False
        },
        timeout=120              # llama3 can be slow, give it time
    )

    result = response.json()
    raw = result["response"]

    # Parse and pretty print JSON
    try:
        parsed = json.loads(raw)
        print("===== AI RCA RESULT =====")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print("===== RAW RESPONSE =====")
        print(raw)

except Exception as e:
    print("Ollama call failed:", str(e))