# launch_dashboard.py
import socket
from nicegui import ui
from dashboard import create_dashboard

def get_primary_ip():
    """Determine the primary IP address of the server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("1.1.1.1", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

host_ip = get_primary_ip()

if __name__ in {"__main__", "__mp_main__"}:
    create_dashboard(host_ip)
    ui.run(port=8080, reload=True, host=host_ip)
