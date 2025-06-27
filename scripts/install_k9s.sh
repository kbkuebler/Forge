#!/bin/bash
set -euo pipefail

VERSION="v0.50.6"
URL="https://github.com/derailed/k9s/releases/download/${VERSION}/k9s_Linux_amd64.tar.gz"
FILENAME="k9s_Linux_amd64.tar.gz"
TMP_DIR="/tmp/k9s-install"

echo "[INFO] Installing k9s ${VERSION}..."

mkdir -p "${TMP_DIR}"
curl -L "${URL}" -o "${TMP_DIR}/${FILENAME}"
tar -xzf "${TMP_DIR}/${FILENAME}" -C "${TMP_DIR}"

if [ ! -f "${TMP_DIR}/k9s" ]; then
    echo "[ERROR] k9s binary not found after extraction"
    exit 1
fi

sudo mv "${TMP_DIR}/k9s" /usr/local/bin/k9s
sudo chmod +x /usr/local/bin/k9s

rm -rf "${TMP_DIR}"

echo "[INFO] ✅ k9s ${VERSION} installed successfully. Run 'k9s' to get started."

