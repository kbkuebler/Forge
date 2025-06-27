#!/bin/bash
set -e

echo "📦 Installing k3s..."

# Skip if already running
if command -v k3s &>/dev/null && systemctl is-active --quiet k3s; then
    echo "✅ k3s already installed and running"
    exit 0
fi

# Install K3s (writes kubeconfig with world-readable perms for simplicity)
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--write-kubeconfig-mode 644" sh -

# Optional: export kubeconfig if in interactive shell
if [ -t 1 ]; then
    echo "📁 Setting KUBECONFIG for current session..."
    export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
    echo "To persist, add this to your shell rc file:"
    echo "export KUBECONFIG=/etc/rancher/k3s/k3s.yaml"
fi

# Final status
echo "✅ k3s installed successfully"
k3s --version

# Copy kubeconfig to ~/.kube/config if running as non-root
mkdir -p "$HOME/.kube"
cp /etc/rancher/k3s/k3s.yaml "$HOME/.kube/config"
chown "$(id -u):$(id -g)" "$HOME/.kube/config"

# Make sure KUBECONFIG is set
export KUBECONFIG="$HOME/.kube/config"

echo "📁 kubeconfig copied to ~/.kube/config"
echo "📌 KUBECONFIG set for this session"

