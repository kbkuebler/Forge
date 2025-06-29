#!/bin/bash
set -e

echo "Installing kubectl..."

# Check if kubectl is already installed
if command -v kubectl &> /dev/null; then
    echo "kubectl already installed: $(kubectl version --client --short)"
    exit 0
fi

# Download latest stable version
KUBECTL_VERSION=$(curl -sL https://dl.k8s.io/release/stable.txt)
echo "Downloading kubectl version $KUBECTL_VERSION..."

curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"

chmod +x kubectl
sudo mv kubectl /usr/local/bin/

echo "kubectl installed successfully: $(kubectl version --client --short)"

