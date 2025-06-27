from nicegui import ui
from dashboard import create_dashboard

if __name__ in {"__main__", "__mp_main__"}:
    create_dashboard()
    ui.run(port=8080, reload=True, host='0.0.0.0')

