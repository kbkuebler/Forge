#!/usr/bin/env python3

import yaml
from typing import Dict, List
from pathlib import Path


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def build_scrape_config(config: dict) -> List[Dict]:
    scrape_configs = []

    # Prometheus itself
    scrape_configs.append({
        "job_name": "prometheus",
        "static_configs": [
            {
                "targets": ["localhost:9090"]
            }
        ]
    })

    for cluster in config.get("clusters", []):
        name = cluster.get("name", "unknown")
        ip = cluster.get("cluster_ip", "0.0.0.0")

        scrape_configs.append({
            "job_name": "cluster",
            "static_configs": [
                {
                    "targets": [
                        f"{ip}:9101",
                        f"{ip}:9102",
                        f"{ip}:9103"
                    ],
                    "labels": {
                        "cluster": name,
                        "instance": name,
                        "node_type": "clusterip"
                    }
                }
            ]
        })

        # Anvil nodes
        anvil_ips = cluster.get("discovered", {}).get("anvil", [])
        if anvil_ips:
            scrape_configs.append({
                "job_name": "anvil_nodes",
                "static_configs": [
                    {
                        "targets": [f"{ip}:9100" for ip in anvil_ips],
                        "labels": {
                            "cluster": name,
                            "instance": f"{name}-anvil",
                            "node_type": "anvil"
                        }
                    }
                ]
            })

        # DSX nodes
        dsx_ips = cluster.get("discovered", {}).get("dsx", [])
        if dsx_ips:
            scrape_configs.append({
                "job_name": "dsx_nodes",
                "static_configs": [
                    {
                        "targets": [f"{ip}:9100" for ip in dsx_ips] +
                                   [f"{ip}:9105" for ip in dsx_ips],
                        "labels": {
                            "cluster": name,
                            "instance": f"{name}-dsx",
                            "node_type": "dsx"
                        }
                    }
                ]
            })

    return scrape_configs


def write_prometheus_config(output_path: Path, scrape_configs: List[Dict]) -> None:
    full_config = {
        "global": {
            "scrape_interval": "15s",
            "evaluation_interval": "15s",
            "scrape_timeout": "10s"
        },
        "alerting": {
            "alertmanagers": [
                {
                    "static_configs": [
                        {"targets": []}
                    ]
                }
            ]
        },
        "rule_files": [
            "/etc/prometheus/rules/*.rules"
        ],
        "scrape_configs": scrape_configs
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(full_config, f, sort_keys=False)


def main():
    config = load_config()
    scrape_configs = build_scrape_config(config)
    output_path = Path("kustomize/prometheus/generated/prometheus.yml")
    write_prometheus_config(output_path, scrape_configs)
    print(f"✓ Generated {output_path}")


if __name__ == "__main__":
    main()

