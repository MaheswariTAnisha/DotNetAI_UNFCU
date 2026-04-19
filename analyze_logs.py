import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read logs
try:
    with open("pipeline.log", "r") as f:
        logs = f.read()
except:
    logs = "No logs found"

# Limit log size (important)
logs = logs[:5000]

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
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    print("===== AI RCA RESULT =====")
    print(response.output_text)

except Exception as e:
    print("AI Analysis Failed:", str(e))