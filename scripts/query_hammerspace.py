#!/usr/bin/env python3

import yaml
import requests
import logging
from typing import Dict, List
from requests.auth import HTTPBasicAuth

# Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("hs-discovery")
requests.packages.urllib3.disable_warnings()


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def discover_nodes(cluster_ip: str, auth: HTTPBasicAuth) -> List[Dict]:
    url = f"https://{cluster_ip}:8443/mgmt/v1.2/rest/nodes"
    try:
        response = requests.get(url, auth=auth, verify=False, timeout=10)
        response.raise_for_status()
        return response.json()  # The top-level response *is* a list
    except Exception as e:
        logger.error(f"Error querying cluster at {cluster_ip}: {e}")
        return []


def extract_node_ips(nodes: List[Dict]) -> Dict[str, List[str]]:
    result = {"anvil": [], "dsx": []}
    seen_ips = set()

    for node in nodes:
        try:
            role = node.get("productNodeType", "").lower()
            ip_info = node.get("mgmtIpAddress", {})
            ip = ip_info.get("address")
            if ip and ip not in seen_ips:
                if "anvil" in role:
                    result["anvil"].append(ip)
                elif "dsx" in role:
                    result["dsx"].append(ip)
                seen_ips.add(ip)
        except Exception as e:
            logger.warning(f"Failed to parse node: {e}")

    return result


def main() -> None:
    config = load_config()

    username = config.get("hammerspace", {}).get("username")
    password = config.get("hammerspace", {}).get("password")
    if not username or not password:
        logger.error("Missing Hammerspace credentials in config.yaml")
        return

    auth = HTTPBasicAuth(username, password)
    output: Dict[str, Dict[str, List[str]]] = {}

    for cluster in config.get("clusters", []):
        name = cluster.get("name")
        ip = cluster.get("cluster_ip")
        if not name or not ip:
            logger.warning("Skipping incomplete cluster entry")
            continue

        logger.info(f"Querying {name} at {ip}...")
        nodes = discover_nodes(ip, auth)
        roles = extract_node_ips(nodes)
        output[name] = roles

    logger.info("Discovered nodes:")
    for cluster, roles in output.items():
        logger.info(f"{cluster}:")
        for role, ips in roles.items():
            logger.info(f"  {role}: {', '.join(ips) or 'none'}")


if __name__ == "__main__":
    main()

