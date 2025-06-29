t's too long to list here, so check out [[Helpful Hammerspace Commands]]

### Set up serviceadmin
First, log into the host as `sysadmin`
You'll then run `serviceadmin-enable`

Now, once you've gotten the temporary password from `supgen`, then you can log in:
```shell
Hammerspace 5.1.24-1328  
Current Date: 2025-06-23  
System S/N: 862c4c6e8a66  
Node Name: forge.twocupsof.coffee  
serviceadmin@192.168.100.200's password:    
  
  
Gathering system information...  
  
Managed capacity:  
-----  
Total:                   85.8GB  
Used:                    636.9MB  
Free:                    85.2GB  
  
Uncleared warning or higher events:  
-----  
WARNING for cluster: Metadata backup is not configured  
       Use 'event-list --uncleared --severity WARNING' to see full details
```



When you want to `ssh` to a DSX from an Anvil, you can enable this by running:

`hssh config`

This will run through and set up the necessary keys. You can then ssh via shortcuts like so:

`ssh d0` for the first DSX, `ssh m1` for the second Anvil, etc.


## See your exports

It's worth noting that you can see all of the Hammerspace exports.

First, make sure to log in as `serviceadmin` and then `ls /hs`.

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

## Check the status of your system

When logged in as `serviceadmin`, you simply run `monitor` on your system to see critical system statistics:
![[Pasted image 20250623101443.png]]
