#!/usr/bin/env python3

import sys
import yaml
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONFIG_FILE = "config.yaml"

def fail(message):
    print(f"[ERROR] {message}")
    sys.exit(1)

def validate_yaml(file_path):
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return data
    except yaml.YAMLError as e:
        fail(f"Invalid YAML syntax: {e}")
    except FileNotFoundError:
        fail(f"{file_path} not found.")
    return None

def check_not_empty(key_name, value):
    if not isinstance(value, str) or not value.strip():
        fail(f"Missing or empty value for '{key_name}' in config.yaml")

def validate_keys(config):
    try:
        cluster = config['clusters'][0]
        check_not_empty("clusters[0].name", cluster.get('name', ''))
        check_not_empty("clusters[0].cluster_ip", cluster.get('cluster_ip', ''))

        hammerspace = config['hammerspace']
        check_not_empty("hammerspace.username", hammerspace.get('username', ''))
        check_not_empty("hammerspace.password", hammerspace.get('password', ''))

        return cluster['name'], cluster['cluster_ip'], hammerspace['username'], hammerspace['password']
    except (KeyError, IndexError):
        fail("Missing expected structure in config.yaml")

def test_hammerspace_api(ip, username, password):
    url = f"https://{ip}:8443/mgmt/v1.2/rest/nodes"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False, timeout=10)
        if response.status_code != 200:
            fail(f"Hammerspace API responded with HTTP {response.status_code}")
        if not isinstance(response.json(), list):
            fail("Unexpected response structure from Hammerspace API")
        print("Successfully connected to Hammerspace API and retrieved node list.")
    except requests.exceptions.RequestException as e:
        fail(f"API request failed: {e}")

if __name__ == "__main__":
    config = validate_yaml(CONFIG_FILE)
    name, cluster_ip, username, password = validate_keys(config)
    print(f"Validated config keys for cluster '{name}' at {cluster_ip}")
    test_hammerspace_api(cluster_ip, username, password)

