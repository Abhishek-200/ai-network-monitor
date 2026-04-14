import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from db.database import init_db, get_recent_logs, get_recent_alerts

app = FastAPI(title="AI Network Monitor")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    logs = await get_recent_logs(10)
    alerts = await get_recent_alerts(5)

    logs_html = ""
    for log in logs:
        color = "red" if log[9] else "green"
        logs_html += f"""
        <tr>
            <td>{log[1]}</td>
            <td>{log[2]}</td>
            <td>{log[3]}</td>
            <td>{log[6]}%</td>
            <td>{log[7]}%</td>
            <td style="color:{color}">
                {"🚨 ANOMALY" if log[9] else "✅ NORMAL"}
            </td>
        </tr>"""

    alerts_html = ""
    for alert in alerts:
        alerts_html += f"""
        <tr>
            <td>{alert[1]}</td>
            <td>{alert[3]}</td>
            <td>{alert[2][:100]}...</td>
        </tr>"""

    return f"""
    <html>
    <head>
        <title>AI Network Monitor</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body {{ font-family: Arial; background: #0f0f0f; color: #fff; padding: 20px; }}
            h1 {{ color: #00ff88; }}
            h2 {{ color: #00aaff; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
            th {{ background: #1a1a2e; padding: 10px; text-align: left; color: #00ff88; }}
            td {{ padding: 8px; border-bottom: 1px solid #333; font-size: 13px; }}
            tr:hover {{ background: #1a1a1a; }}
        </style>
    </head>
    <body>
        <h1>🤖 AI Network Monitor Dashboard</h1>
        <p>Auto-refreshes every 30 seconds</p>
        <h2>📊 Recent Network Logs</h2>
        <table>
            <tr>
                <th>Timestamp</th>
                <th>Bytes Sent</th>
                <th>Bytes Recv</th>
                <th>CPU</th>
                <th>Memory</th>
                <th>Status</th>
            </tr>
            {logs_html}
        </table>
        <h2>🚨 Recent Alerts</h2>
        <table>
            <tr>
                <th>Timestamp</th>
                <th>Severity</th>
                <th>Analysis</th>
            </tr>
            {alerts_html}
        </table>
    </body>
    </html>
    """

@app.get("/api/logs")
async def get_logs():
    logs = await get_recent_logs(20)
    return {"logs": logs}

@app.get("/api/alerts")
async def get_alerts():
    alerts = await get_recent_alerts(10)
    return {"alerts": alerts}
