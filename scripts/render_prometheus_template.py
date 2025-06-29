#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import yaml
from pathlib import Path

# Load config.yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

# Jinja2 setup
template_path = Path("templates")
env = Environment(loader=FileSystemLoader(template_path))
template = env.get_template("prometheus.yml.j2")

# Render with variables
rendered = template.render(
    global_config=config.get("global", {}),
    clusters=config.get("clusters", [])
)

# Write output
output_path = Path("kustomize/prometheus/generated/prometheus.yml")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    f.write(rendered)

print(f"Rendered Prometheus config to {output_path}")

