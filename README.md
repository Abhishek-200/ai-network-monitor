# 🤖 AI Network Monitor

An autonomous AI agent that monitors network traffic on AWS EC2,
analyzes metrics using Groq LLaMA AI, and detects anomalies in real time.

## 🚀 Tech Stack
- Python 3 - Core language
- Groq LLaMA AI - Anomaly detection & analysis
- FastAPI - Web dashboard
- SQLite - Data storage
- psutil - Network & system metrics
- AWS EC2 - Cloud deployment

## 🧠 How It Works
1. Agent collects network metrics every 30 seconds
2. Sends data to Groq LLaMA AI for analysis
3. AI decides if traffic is NORMAL or ANOMALY
4. Anomalies are saved and displayed on dashboard
5. Slack alerts sent for critical issues

## 📊 Features
- Real-time network monitoring
- AI-powered anomaly detection
- Live web dashboard
- Alert history
- Fully automated agent

## ▶️ How to Run
1. Clone the repo
2. Create .env with your GROQ_API_KEY
3. pip install -r requirements.txt
4. python3 agent/main_agent.py
5. uvicorn api.main:app --host 0.0.0.0 --port 8000


## 📸 Screenshots

### AI Dashboard
![Dashboard](dashboard.png)
