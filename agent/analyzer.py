from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

async def analyze_network(summary: str) -> dict:
    prompt = f"""
You are an expert network security analyst and DevOps engineer.
Analyze the following network metrics and determine if anything is suspicious or abnormal.

{summary}

Respond in this exact format:
STATUS: NORMAL or ANOMALY
SEVERITY: LOW, MEDIUM, or HIGH
ANALYSIS: (2-3 sentences explaining what you see)
ACTION: (what should be done if anything)
"""

    response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    result = response.choices[0].message.content

    is_anomaly = "ANOMALY" in result
    severity = "LOW"
    if "SEVERITY: HIGH" in result:
        severity = "HIGH"
    elif "SEVERITY: MEDIUM" in result:
        severity = "MEDIUM"

    return {
        "analysis": result,
        "is_anomaly": is_anomaly,
        "severity": severity
    }
