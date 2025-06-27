#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}[*] Creating SE Toolkit project structure...${NC}"

mkdir -p scripts
mkdir -p secrets
mkdir -p dashboard
mkdir -p kustomize
mkdir -p kustomize/prometheus
mkdir -p kustomize/loki
mkdir -p kustomize/vector
mkdir -p kustomize/csi-driver
mkdir -p kustomize/grafana
mkdir -p kustomize/base  # Optional: for shared configmaps/secrets, etc.

touch config.yaml
touch requirements.txt

# Create starter .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo ".venv/" > .gitignore
    echo -e "${GREEN}[*] Created .gitignore with .venv/${NC}"
elif ! grep -qxF ".venv/" .gitignore; then
    echo ".venv/" >> .gitignore
    echo -e "${GREEN}[*] Appended .venv/ to .gitignore${NC}"
fi

echo -e "${GREEN}[✓] Directory structure created.${NC}"

