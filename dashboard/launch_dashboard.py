from nicegui import ui
from dashboard import create_dashboard
import socket

# Get server address for external access links
host_ip = os.environ.get('SERVER_ADDRESS', 'localhost')

#Let's try this to get a dynamic server address
def get_primary_ip():
    try:
        # Use a UDP socket to a public IP to determine the outbound interface
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("1.1.1.1", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"  # fallback if something goes wrong

host_ip = get_primary_ip()

if __name__ in {"__main__", "__mp_main__"}:
    create_dashboard()
    ui.run(port=8080, reload=True, host=host_ip)

