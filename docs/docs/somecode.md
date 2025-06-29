```yaml

---
cluster:
  cluster_name: hs-poc-test
  dns_servers:
    - 192.168.1.2
  domainname: onaside.quest
  gateway:
    ipv4_default: 192.168.122.1
  ntp_servers:
    - 129.6.15.29 # Hammerspace does not support pooled ntp
  password: 1Hammerspace! # There needs to be at least one non alphanumeric character
  metadata:
    ips:
      - 192.168.122.50/24 # This should  be your cluster IP
```

There you go!
