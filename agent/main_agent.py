import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.collector import get_network_metrics, get_network_summary
from agent.analyzer import analyze_network
from agent.alerter import send_slack_alert
from db.database import init_db, save_log, save_alert

MONITOR_INTERVAL = 30

async def run_agent():
    print("🚀 AI Network Monitor Agent Started!")
    print("Initializing database...")
    await init_db()
    print("✅ Database ready!")
    print(f"Monitoring every {MONITOR_INTERVAL} seconds...\n")

    while True:
        try:
            print("📊 Collecting network metrics...")
            metrics = get_network_metrics()
            summary = get_network_summary(metrics)
            print(summary)

            print("🤖 Analyzing with Claude AI...")
            result = await analyze_network(summary)

            print(f"AI Analysis:\n{result['analysis']}")
            print(f"Anomaly Detected: {result['is_anomaly']}")
            print(f"Severity: {result['severity']}\n")

            metrics['ai_analysis'] = result['analysis']
            metrics['is_anomaly'] = 1 if result['is_anomaly'] else 0
            await save_log(metrics)

            if result['is_anomaly']:
                await save_alert(
                    metrics['timestamp'],
                    result['analysis'],
                    result['severity']
                )
                send_slack_alert(
                    result['analysis'],
                    result['severity'],
                    metrics['timestamp']
                )
                print(f"🚨 Alert saved and sent!")

            print(f"✅ Cycle complete. Waiting {MONITOR_INTERVAL}s...\n")
            print("-" * 50)
            await asyncio.sleep(MONITOR_INTERVAL)

        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_agent())
