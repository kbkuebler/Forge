#!/bin/bash
set -e

BASHRC="$HOME/.bashrc"
PROJECT_DIR="$(pwd)"

echo "✨ Adding convenience functions to $BASHRC..."

# Auto-activate .venv
if ! grep -q "source $PROJECT_DIR/.venv/bin/activate" "$BASHRC"; then
  echo -e "\n# Auto-activate Forge Toolkit virtualenv" >> "$BASHRC"
  echo "if [ -f \"$PROJECT_DIR/.venv/bin/activate\" ]; then" >> "$BASHRC"
  echo "  source \"$PROJECT_DIR/.venv/bin/activate\"" >> "$BASHRC"
  echo "fi" >> "$BASHRC"
fi

# Set KUBECONFIG
if ! grep -q "export KUBECONFIG=\$HOME/.kube/config" "$BASHRC"; then
  echo -e "\n# Set default kubeconfig for k3s" >> "$BASHRC"
  echo "export KUBECONFIG=\$HOME/.kube/config" >> "$BASHRC"
fi

# kubectl autocomplete
if ! grep -q "source <(kubectl completion bash)" "$BASHRC"; then
  echo -e "\n# Enable kubectl bash completion" >> "$BASHRC"
  echo "source <(kubectl completion bash)" >> "$BASHRC"
fi

echo "✅ Shell helpers added. You can run 'source ~/.bashrc' or open a new terminal."

