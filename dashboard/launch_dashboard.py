from nicegui import ui
from dashboard import create_dashboard
import socket
from dashboard import get_primary_ip

#Let's try this to get a dynamic server address

host_ip = get_primary_ip()

if __name__ in {"__main__", "__mp_main__"}:
    create_dashboard()
    ui.run(port=8080, reload=True, host=host_ip)

