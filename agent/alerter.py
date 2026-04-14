import requests
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(analysis: str, severity: str, timestamp: str):
    if not SLACK_WEBHOOK_URL:
        print("No Slack webhook configured")
        return

    emoji = "🔴" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"

    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} AI Network Alert - {severity} Severity"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Time:* {timestamp}\n\n*AI Analysis:*\n{analysis}"
                }
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print(f"Alert sent to Slack: {severity}")
        else:
            print(f"Slack error: {response.status_code}")
    except Exception as e:
        print(f"Failed to send alert: {e}")
