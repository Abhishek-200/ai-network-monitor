import aiosqlite
import asyncio

DB_PATH = "network_monitor.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS network_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                bytes_sent INTEGER,
                bytes_recv INTEGER,
                packets_sent INTEGER,
                packets_recv INTEGER,
                cpu_percent REAL,
                memory_percent REAL,
                ai_analysis TEXT,
                is_anomaly INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                alert_message TEXT,
                severity TEXT
            )
        """)
        await db.commit()

async def save_log(data: dict):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO network_logs 
            (timestamp, bytes_sent, bytes_recv, packets_sent, 
             packets_recv, cpu_percent, memory_percent, ai_analysis, is_anomaly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['timestamp'], data['bytes_sent'], data['bytes_recv'],
            data['packets_sent'], data['packets_recv'], data['cpu_percent'],
            data['memory_percent'], data['ai_analysis'], data['is_anomaly']
        ))
        await db.commit()

async def save_alert(timestamp: str, message: str, severity: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO alerts (timestamp, alert_message, severity) VALUES (?, ?, ?)",
            (timestamp, message, severity)
        )
        await db.commit()

async def get_recent_logs(limit: int = 20):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM network_logs ORDER BY id DESC LIMIT ?", (limit,)
        ) as cursor:
            return await cursor.fetchall()

async def get_recent_alerts(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,)
        ) as cursor:
            return await cursor.fetchall()
