# This is where we can put links, config files, and info.


```shell
08-20 22:02:02 anvil-site-a ~ $ ls -1 /hs  
bar  
csi-pvc-32ede17b-2a75-4298-b62e-92944f5e2047  
csi-pvc-b56600f7-798b-40be-9d52-e1ba23432fa4  
csi-pvc-ce613eeb-a1bd-4660-9153-d29284565275  
csi-pvc-d741d843-20f5-46ba-b6f3-ea9400096d8f  
csi-pvc-e5a8a85c-a850-4c56-bd31-a469959163cd  
csi-pvc-ef49bd76-d5c2-45ea-9d1c-a0628fd7f4f9  
goodtimes  
k8s  
k8s-block-storage  
k8s-files  
k8s-file-storage  
pvc-3c568a44-c473-4f78-aaf5-8523e4cf93ce
```


### Summary

We have a working k3s environment with Vector for log ingestion, Loki for log aggregation, Prometheus for metrics, Grafana for visualization, the Hammerspace CSI driver for storage, and NiceGUI as a UI. Both Fluent Bit and Vector were evaluated for logging, with Vector chosen for its flexibility and features—for now. The Python SDK example enables programmatic share creation, demonstrating automation potential. This setup forms a foundation for Hammerspace POCs and lab work, with room to revisit and improve as needed.

I'm hoping that eventually, we have team collaboration that will allow for some performance testing, reporting, etc.

### Accomplishments Thus Far

- **Kubernetes Cluster:**  k3s deployed as the platform foundation.

- **Logging & Monitoring:** Evaluated Fluent Bit and Vector; currently using Vector for syslog ingestion and processing.

- **Storage Integration:** Hammerspace CSI driver installed and functioning. The NFS CSI driver is also installed currently simply for comparison.

- **Automation & SDK:** Python SDK with a share creation example working well.

- **User Interface:** NiceGUI web interface. Chosen because it seems that several SEs are already comfortable with Python and the framework makes it easy to rapidly iterate.

- **Configuration & Deployment:** Helm or Kustomize with manifests managing the stack for ease of updates.

### Suggested Next Steps to Add Value for Hammerspace POCs

- Create a bootstrap script that deploys the entire stack. This could also make it suitable for Skillable use.

- Use the SDK to interrogate cluster info. Use the results to generate scrape configs for tprometheus.

- Create dashboards that are a bit more appropriate for customer consumption. The existing dashboards may be a bit much for new users. 

- Revisit Fluent-bit and see what will transform our syslog messages in the simplest way possible.

- Create a Helm chart or kustomize overlay for the entire stack (CSI driver + monitoring + UI) to simplify deployment and updates.

- Integrate alerting rules in Prometheus for key storage events or health status.

- Document the environment, architecture, and demo scenarios clearly for SEs to quickly replicate and customize. This could be added right into the stack if we wanted.

- Add FIO and Hammerspace performance toolkit so we 
