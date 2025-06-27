#!/usr/bin/env python3

from pathlib import Path
import yaml
import base64

# File paths
CONFIG_PATH = Path("config.yaml")
OUTPUT_PATH = Path(".generated/csi-secret.yaml")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Load config.yaml
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Extract credentials
hs_config = config.get("hammerspace", {})
username = hs_config.get("username", "")
password = hs_config.get("password", "")

# Extract first cluster IP and build endpoint
clusters = config.get("clusters", [])
if not clusters or "cluster_ip" not in clusters[0]:
    raise ValueError("Missing 'cluster_ip' in config.yaml['clusters'][0]")

endpoint = f"https://{clusters[0]['cluster_ip']}"

# Base64 encode credentials
def b64_encode(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")

# Build Secret manifest
secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {
        "name": "com.hammerspace.csi.credentials",
        "namespace": "kube-system"
    },
    "type": "Opaque",
    "data": {
        "username": b64_encode(username),
        "password": b64_encode(password),
    },
    "stringData": {
        "endpoint": endpoint
    }
}

# Write the secret file
with open(OUTPUT_PATH, "w") as f:
    yaml.dump(secret, f, sort_keys=False)

print(f"Secret written to {OUTPUT_PATH}")

