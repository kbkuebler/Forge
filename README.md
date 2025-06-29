# Forge

A modular and lightweight observability stack built for system engineers using modern tools like:
- **k3s**: Lightweight Kubernetes
- **NiceGUI**: Python UI framework
- **Fluent Bit**: Log/data collector and forwarder
- **Loki + Grafana**: Log aggregation and visualization
- **Kustomize**: Kubernetes configuration management
- **BASH + Python**: Scripting and orchestration

## Features

- Centralized logging with **Loki**
- Real-time dashboards using **Grafana**
- Log routing and transformation with **Fluent Bit**
- Custom admin interface with **NiceGUI**
- Deployed via **k3s** and managed using **Kustomize**
- MkDocs for distributing pertinent information
- Designed for simplicity, modularity, and maintainability


## Prerequisites
- An Ubuntu 24.04 system
- Root access or sudo privileges
- SSH access to the VM
- A configured Hammerspace cluster with metrics enabled and syslog configured

To configure Hammerspace metrics, log in to your Anvil node and run the following commands:
```bash
admin@forge.twocupsof.coffee> cluster-config --prometheus-exporters-enable 
```
Then you can run the following command to configure syslog:
```bash
admin@forge.twocupsof.coffee> syslog-config --enable --server 192.168.1.23,32424,tcp,event|filesystem
```

**_NOTE:_**  Replace 192.168.1.23 with the IP address of your syslog server. Port 32424 is the default port for fluent-bit.



## Installation

First clone the repository:
```bash
git clone https://github.com/kbkuebler/Forge.git
``` 

Then run the modify the config.yaml file to match your environment:
```bash
clusters:
  - name: forge.twocupsof.coffee
    cluster_ip: 192.168.100.200
    ports:
      metrics: 9100
      api: 9101
      c_metrics: 9102
      c_advisor: 9103
    labels:
      env: lab
      region: east
```

Then run the bootstrap script:
```bash
./bootstrap.sh
```

This will install all the necessary tools and deploy the observability stack to your cluster.
You should then be able to access the admin interface at http://localhost:8080.