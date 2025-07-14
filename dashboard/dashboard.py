import os
from datetime import datetime
import socket

from kubernetes import client, config
from kubernetes.client import CoreV1Api, AppsV1Api
from nicegui import ui

# Configure Kubernetes client
config.load_kube_config()
v1 = CoreV1Api()
apps_v1 = AppsV1Api()

# Get server address for external access links
SERVER_ADDRESS = os.environ.get('SERVER_ADDRESS', 'localhost')

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

# Define services
SERVICES = {
    'grafana': {'port': 32000, 'deployment': 'grafana', 'namespace': 'hammerspace'},
    'prometheus': {'port': 30090, 'deployment': 'prometheus', 'namespace': 'hammerspace'},
    'loki': {'port': 32002, 'deployment': 'loki', 'namespace': 'hammerspace'},
    'fluent-bit': {'port': 32424, 'deployment': 'fluent-bit', 'namespace': 'hammerspace'},
    'csi-nfs-node': {'port': None, 'deployment': 'csi-node', 'namespace': 'kube-system', 'type': 'daemonset'},
    'mkdocs': {'port': 32010, 'deployment': None, 'namespace': None, 'type': 'static'}
}


def get_service_status(service_name):
    service = SERVICES[service_name]
    is_daemonset = service.get('type') == 'daemonset'

    if service.get('type') == 'static':
        return {
            'name': service_name,
            'port': service['port'],
            'status': 'Available',
            'replicas': 1,
            'available_replicas': 1,
            'type': 'Static Service',
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'versions': []
        }

    status = {
        'name': service_name,
        'port': service['port'],
        'status': 'Unknown',
        'replicas': 0,
        'available_replicas': 0,
        'type': 'DaemonSet' if is_daemonset else 'Deployment',
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'versions': []
    }

    try:
        if is_daemonset:
            ds = apps_v1.read_namespaced_daemon_set(service['deployment'], service['namespace'])
            status['replicas'] = ds.status.desired_number_scheduled or 0
            status['available_replicas'] = ds.status.number_available or 0
            status['status'] = 'Running' if status['available_replicas'] > 0 else 'Not Available'

            containers = ds.spec.template.spec.containers
            status['versions'] = [c.image.split(':')[-1] if ':' in c.image else 'latest' for c in containers]

            pods = v1.list_namespaced_pod(
                namespace=service['namespace'],
                label_selector="app.kubernetes.io/name=csi-nfs-node"
            )
            status['pods'] = [
                {
                    'name': pod.metadata.name,
                    'status': pod.status.phase,
                    'node': pod.spec.node_name,
                    'containers': [
                        {
                            'name': c.name,
                            'ready': c.ready,
                            'restart_count': c.restart_count
                        }
                        for c in pod.status.container_statuses or []
                    ]
                }
                for pod in pods.items
            ]
        else:
            deploy = apps_v1.read_namespaced_deployment(service['deployment'], service['namespace'])
            status['replicas'] = deploy.status.replicas or 0
            status['available_replicas'] = deploy.status.available_replicas or 0
            status['status'] = 'Running' if status['available_replicas'] > 0 else 'Not Available'

            containers = deploy.spec.template.spec.containers
            status['versions'] = [c.image.split(':')[-1] if ':' in c.image else 'latest' for c in containers]

    except Exception as e:
        status['error'] = str(e)
        status['status'] = 'Error'

    return status


def create_card_content(service_name, status):
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
                    url = f"http://{SERVER_ADDRESS}:{status['port']}"
                    ui.link("Open", url)
                    ui.link(" (Copy URL)", url, new_tab=False).on("click", lambda e, url=url:
                        ui.run_javascript(f'navigator.clipboard.writeText("{url}")'))

            if 'error' in status:
                ui.label(f"Error: {status['error']}").classes('text-red-500')

            ui.label(f"Last checked: {status['last_update']}").classes('text-xs text-gray-500')


service_cards = {}


def create_card(service_name, status):
    card = ui.card().classes('w-96' if service_name == 'csi-nfs-node' else 'w-80')
    with card:
        create_card_content(service_name, status)
    service_cards[service_name] = card
    return card


def update_all_cards():
    for service_name in SERVICES:
        if SERVICES[service_name].get('type') == 'static':
            continue  # No need to refresh static services
        status = get_service_status(service_name)
        if service_name in service_cards:
            card = service_cards[service_name]
            card.clear()
            with card:
                create_card_content(service_name, status)


def create_dashboard():
    ui.page_title("Hammerspace Forge")
    with ui.header().classes('justify-between items-center bg-blue-600 text-white p-4'):
        ui.label('Hammerspace Forge').classes('text-xl font-bold')
        ui.button('Refresh', icon='refresh').on('click', update_all_cards)\
            .classes('bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded').props('flat')

    with ui.column().classes('w-full p-4'):
        with ui.row().classes('w-full justify-end mb-2'):
            ui.link("📘 View Documentation", f"http://{SERVER_ADDRESS}:32010")\
                .classes('text-blue-600 underline hover:text-blue-800 text-sm')\
                .props('target=_blank')

        with ui.row().classes('w-full flex-wrap gap-4'):
            for service_name in SERVICES:
                status = get_service_status(service_name)
                create_card(service_name, status)


