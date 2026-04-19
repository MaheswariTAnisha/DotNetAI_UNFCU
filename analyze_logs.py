import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read logs
try:
    with open("pipeline.log", "r") as f:
        logs = f.read()
except:
    logs = "No logs found"

prompt = f"""
You are a DevOps expert.

Analyze this Azure DevOps pipeline failure log.

Provide output in JSON:
- error_type
- root_cause
- fix_suggestion

Log:
{logs}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

print("===== AI RCA RESULT =====")
print(response.choices[0].message.content)