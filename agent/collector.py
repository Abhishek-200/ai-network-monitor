import psutil
import datetime

def get_network_metrics():
    net = psutil.net_io_counters()
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_recv": net.packets_recv,
        "cpu_percent": cpu,
        "memory_percent": memory.percent
    }

def get_network_summary(metrics: dict) -> str:
    mb_sent = metrics['bytes_sent'] / (1024 * 1024)
    mb_recv = metrics['bytes_recv'] / (1024 * 1024)

    return f"""
Network Metrics at {metrics['timestamp']}:
- Data Sent: {mb_sent:.2f} MB
- Data Received: {mb_recv:.2f} MB
- Packets Sent: {metrics['packets_sent']}
- Packets Received: {metrics['packets_recv']}
- CPU Usage: {metrics['cpu_percent']}%
- Memory Usage: {metrics['memory_percent']}%
"""
