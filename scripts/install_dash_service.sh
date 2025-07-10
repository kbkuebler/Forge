#!/bin/bash
### This will install the dashboard as a systemd service
set -e

SERVICE_NAME=forge-dashboard
DASHBOARD_DIR=$FORGE_DIR/dashboard
UNIT_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PYTHON_EXEC="${FORGE_DIR}/.venv/bin/python3"

USER_NAME=$(whoami)

echo $PYTHON_EXEC
echo "[+] Installing ${SERVICE_NAME} as a systemd service..."

# Create systemd unit file
sudo tee "$UNIT_FILE" > /dev/null <<EOF
[Unit]
Description=Forge Dashboard (NiceGUI)
After=network.target

[Service]
ExecStart=${PYTHON_EXEC} ${DASHBOARD_DIR}/launch_dashboard.py
WorkingDirectory=${DASHBOARD_DIR}
Restart=always
User=${USER_NAME}
Environment=SERVER_ADDRESS=localhost

[Install]
WantedBy=multi-user.target
EOF

echo "Service unit written to ${UNIT_FILE}"

# Reload systemd and start the service
echo "Reloading systemd daemon and enabling service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable --now "${SERVICE_NAME}"

echo "${SERVICE_NAME} is now running. Access it at http://localhost:8080"