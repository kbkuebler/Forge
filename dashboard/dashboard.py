# dashboard.py
import os
from datetime import datetime
from kubernetes import client, config
from kubernetes.client import CoreV1Api, AppsV1Api
from nicegui import ui

# Kubernetes client setup
config.load_kube_config()
v1 = CoreV1Api()
apps_v1 = AppsV1Api()

# Define services
SERVICES = {
    'grafana': {'port': 32000, 'deployment': 'grafana', 'namespace': 'hammerspace'},
    'prometheus': {'port': 30090, 'deployment': 'prometheus', 'namespace': 'hammerspace'},
    'loki': {'port': 32002, 'deployment': 'loki', 'namespace': 'hammerspace'},
    'fluent-bit': {'port': 32424, 'deployment': 'fluent-bit', 'namespace': 'hammerspace'},
    'csi-nfs-node': {'port': None, 'deployment': 'csi-node', 'namespace': 'kube-system', 'type': 'daemonset'},
    'mkdocs': {'port': 32010, 'deployment': None, 'namespace': None, 'type': 'static'}
}

service_cards = {}

def get_service_status(service_name):
    # (same as your current version, no changes needed here)
    ...

def create_card_content(service_name, status, server_address):
    is_csi = service_name == 'csi-nfs-node'

    with ui.column().classes('w-full'):
        with ui.row().classes('w-full justify-between items-center'):
            ui.label(service_name).classes('text-lg font-bold')
            ui.label(status['status']).classes(
                f'px-2 py-1 rounded text-white ' +
                ('bg-green-500' if status['status'] in {'Running', 'Available'} else
                 'bg-yellow-500' if status['status'] == 'Not Available' else
                 'bg-red-500')
            )

        ui.badge(status['type'], color='blue').props('dense outline')

        if status['versions']:
            ui.label(f"Version(s): {', '.join(status['versions'])}")

        ui.separator()

        with ui.column():
            if is_csi:
                ui.label(f"Nodes: {status['available_replicas']}/{status['replicas']}")

            if service_name in {'grafana', 'prometheus', 'mkdocs'} and status['port']:
                with ui.row().classes('items-center'):
                    ui.label("Access:")
                    url = f"http://{server_address}:{status['port']}"
                    ui.link("Open", url)
                    ui.link(" (Copy URL)", url, new_tab=False).on("click", lambda e, url=url:
                        ui.run_javascript(f'navigator.clipboard.writeText("{url}")'))

            if 'error' in status:
                ui.label(f"Error: {status['error']}").classes('text-red-500')

            ui.label(f"Last checked: {status['last_update']}").classes('text-xs text-gray-500')


def create_card(service_name, status, server_address):
    card = ui.card().classes('w-96' if service_name == 'csi-nfs-node' else 'w-80')
    with card:
        create_card_content(service_name, status, server_address)
    service_cards[service_name] = card
    return card


def update_all_cards(server_address):
    for service_name in SERVICES:
        if SERVICES[service_name].get('type') == 'static':
            continue
        status = get_service_status(service_name)
        if service_name in service_cards:
            card = service_cards[service_name]
            card.clear()
            with card:
                create_card_content(service_name, status, server_address)


def create_dashboard(server_address):
    ui.page_title("Hammerspace Forge")
    with ui.header().classes('justify-between items-center bg-blue-600 text-white p-4'):
        ui.label('Hammerspace Forge').classes('text-xl font-bold')
        ui.button('Refresh', icon='refresh').on('click', lambda: update_all_cards(server_address))\
            .classes('bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded').props('flat')

    with ui.column().classes('w-full p-4'):
        with ui.row().classes('w-full justify-end mb-2'):
            ui.link("📘 View Documentation", f"http://{server_address}:32010")\
                .classes('text-blue-600 underline hover:text-blue-800 text-sm')\
                .props('target=_blank')

        with ui.row().classes('w-full flex-wrap gap-4'):
            for service_name in SERVICES:
                status = get_service_status(service_name)
                create_card(service_name, status, server_address)
