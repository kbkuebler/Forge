#!/bin/bash
set -e

echo "---------------------------------------------"
echo "Setting up Forge SE Toolkit..."
echo "---------------------------------------------"

echo "---------------------------------------------"
echo "[0] Setting up directories..."
echo "---------------------------------------------"
bash scripts/setup_directories.sh

echo "Directories created..."
# 1. ENVIRONMENT SETUP
echo "[1] Installing Python and requirements..."
bash scripts/install_python.sh

echo "[1] Activating Python virtual environment..."
source .venv/bin/activate

echo "[1] Copying docs to /opt/forge/docs..."
sudo mkdir -p /opt/forge/docs
sudo cp -r ./docs/* /opt/forge/docs/

echo "---------------------------------------------"
echo "[2]Install Kubernetes Tools..."
echo "---------------------------------------------"
# 2. INSTALL KUBERNETES TOOLS
echo "[2] Installing kubectl CLI..."
bash scripts/install_kubectl.sh

echo "[2] Installing k3s Kubernetes..."
bash scripts/install_k3s.sh

echo "[2] Installing k9s..."
bash scripts/install_k9s.sh

echo "---------------------------------------------"
echo "[3]Validating Configurations"
echo "---------------------------------------------"
if [ ! -f config.yaml ]; then
  echo "[3] ERROR: config.yaml is missing. Please create it before running bootstrap.sh"
  exit 1
fi

echo "[3] Querying Hammerspace clusters..."
python3 scripts/query_hammerspace.py

echo "---------------------------------------------"
echo "[4]Generating Configs"
echo "---------------------------------------------"

echo "[4] Generating Prometheus scrape config..."
python3 scripts/generate_scrape_config.py

echo "[4] Generating CSI Secret from config.yaml..."
python3 scripts/generate_csi_secret_yaml.py

#echo "[4] Moving generated Prometheus config into place..."
#cp .generated/prometheus.yaml kustomize/prometheus/configmap.yaml

echo "[4] Moving CSI secret into kustomize/csi-driver/..."
mv -f .generated/csi-secret.yaml kustomize/csi-driver/csi-secret.yaml

echo "---------------------------------------------"
echo "[5] Deploying Kustomize Stack"
echo "---------------------------------------------"

echo "[5] Creating base namespace..."
kubectl apply -k kustomize/base

echo "[5] Deploying Hammerspace CSI Driver..."
kubectl apply -k kustomize/csi-driver

echo "[5] Deploying Prometheus..."
kubectl apply -k kustomize/prometheus

echo "[5] Deploying Loki..."
kubectl apply -k kustomize/loki

echo "[5] Deploying Fluent Bit..."
kubectl apply -k kustomize/fluent-bit

echo "[5] Deploying Grafana..."
kubectl apply -k kustomize/grafana

echo "[5] Deploying MkDocs..."
kubectl apply -k kustomize/mkdocs

echo "---------------------------------------------"
echo "[6] Adding shell helpers..."
echo "---------------------------------------------"

bash scripts/setup_shell_helpers.sh

echo "---------------------------------------------"
echo "[7] Launching SE Dashboard..."
echo "---------------------------------------------
"
export SERVER_ADDRESS=$(hostname -I | awk '{print $1}')
python3 dashboard/launch_dashboard.py &

# 8. DONE
echo "Forge setup complete."
echo "---------------------------------------------"
echo "Dashboard:     http://$SERVER_ADDRESS:8080"
echo "Grafana:       http://$SERVER_ADDRESS:32000"
echo "Prometheus:    http://$SERVER_ADDRESS:32001"
echo "Documentation: http://$SERVER_ADDRESS:32010"
echo "\m/"

