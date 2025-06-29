## Preparation

This guide is assuming that you already have a functioning `KVM/qemu/libvirt` environment.

First, we'll prepare our installer file that has the relevant Hammerspace information. You should have:

- Host names
- Number of nodes in the cluster
- Cluster name
- IP addresses
- Any hardware specific requirements

## Create and prepare `installer.yaml` for Hammerspace cluster configuration

Use the following file as a template for your cluster, modifying as necessary for your environment.

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

node_index: "0" # This is what will determine wich node spec to use.
nodes:
  "0":
    features:
      - metadata # Metadata will tell the node that it's an Anvil
    ha_mode: Primary
    hostname: hs-anvil-1
    networks:
      eth0:
        cluster_ips:
          - 192.168.122.50
        dhcp: false
        ips:
          - 192.168.122.51/24
        roles:
          - data #Data is for prod traffic
          - ha
          - mgmt
        mtu: 1500
    recover: false
    storage:
      options:
        - raid0
  "1":
    features:
      - metadata
    ha_mode: Secondary # Second node in an HA pair
    hostname: hs-anvil-2
    networks:
      eth0:
        cluster_ips:
          - 192.168.122.50
        dhcp: false
        ips:
          - 192.168.122.52/24
        roles:
          - data # These roles will tell the node that it's a DSX node
          - ha
          - mgmt
        mtu: 1500
    recover: false
    storage:
      options:
        - raid0
  "2":
    features:
      - storage
      - portal
    hostname: hs-dsx-1
    networks:
      eth0:
        cluster_ips:
          - 192.168.122.50
        dhcp: false
        ips:
          - 192.168.122.53/24
        roles:
          - data
          - ha
          - mgmt
        mtu: 1500
  "3":
    features:
      - storage
      - portal
    hostname: hs-dsx-2
    networks:
      eth0:
        cluster_ips:
          - 192.168.122.50
        dhcp: false
        ips:
          - 192.168.122.54/24
        roles:
          - data
          - ha
          - mgmt
        mtu: 1500
version: "1"

```



## Create Configuration Drive to Present Hammerspace Configuration

Once we have this configured, we then need to create an image file that will act as a configuration drive. When the Hammerspace image boots, it peers inside the drives to see if `COPY_TO_HAMMERSPACE` is present on the drive and then will copy the `installer.yaml` to the proper location to use in setting up the cluster.

First, we'll create a file that will be formatted as an `.img` .

`truncate -s 500MB config_drive.img`

We can then  set the proper permissions on the file:

`chmod 644 config_drive.img`

Now we'll format the drive vfat for the sake of compatibility:

`mkfs.vfat -F 32 config_drive.img`

Mount the image and copy/create relevant files:

`mount -o loop config-drive.img /mnt/configdrive

`mkdir /mnt/configdrive/etc `
`touch /mnt/configdrive/COPY_TO_HAMMERSPACE` 
`cp /home/opc/installer.yaml /mnt/configdrive/etc/`  

We can now unmount the drive:

`umount /mnt/configdrive`

Here's a script that will simplify the process.

```bash
#!/bin/bash

# Define variables
IMAGE_FILE="config-drive.img"
MOUNT_POINT="/mnt/configdrive"
INSTALLER_FILE="/home/opc/installer.yaml"

# Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root or with sudo." >&2
    exit 1
fi

# Check if the image file already exists
if [[ -f "$IMAGE_FILE" ]]; then
    echo "Warning: $IMAGE_FILE already exists. Removing it..."
    rm -f "$IMAGE_FILE"
fi

# Create the image file
echo "Creating $IMAGE_FILE with 1GB size..."
truncate -s 1G "$IMAGE_FILE"
chmod 644 "$IMAGE_FILE"

# Format the image with VFAT (FAT32)
echo "Formatting $IMAGE_FILE with VFAT (FAT32)..."
mkfs.vfat -F 32 "$IMAGE_FILE" || { echo "Failed to format $IMAGE_FILE"; exit 1; }

# Create mount point if it doesn't exist
if [[ ! -d "$MOUNT_POINT" ]]; then
    echo "Creating mount point $MOUNT_POINT..."
    mkdir -p "$MOUNT_POINT"
fi

# Mount the image file
echo "Mounting $IMAGE_FILE at $MOUNT_POINT..."
mount -o loop "$IMAGE_FILE" "$MOUNT_POINT" || { echo "Failed to mount $IMAGE_FILE"; exit 1; }

# Create necessary directories and files
echo "Setting up config drive structure..."
mkdir -p "$MOUNT_POINT/etc"
touch "$MOUNT_POINT/COPY_TO_HAMMERSPACE"

# Check if installer file exists before copying
if [[ -f "$INSTALLER_FILE" ]]; then
    echo "Copying $INSTALLER_FILE to $MOUNT_POINT/etc/..."
    cp "$INSTALLER_FILE" "$MOUNT_POINT/etc/" || { echo "Failed to copy $INSTALLER_FILE"; exit 1; }
else
    echo "Warning: $INSTALLER_FILE does not exist. Skipping copy."
fi

# Unmount the image
echo "Unmounting $MOUNT_POINT..."
umount "$MOUNT_POINT" || { echo "Failed to unmount $MOUNT_POINT"; exit 1; }

echo "Config drive setup complete."
```



## Deploying the KVM Virtual Machines

We'll start with the first anvil. Note that the only `installer.yaml` change that needs to be made for each VM is:

 `node_index: "0" `

For example,  to install your first Anvil, you would use:

```shell
node_index: "0" # This is what will determine wich node spec to use.
nodes:
  "0":
    features:
      - metadata # Metadata will tell the node that it's an Anvil
    ha_mode: Primary
    ...
```

To install your second Anvil, simply change the `node_index to 1`:
```shell
node_index: "1" # This is what will determine wich node spec to use.
nodes:
  "0":
    features:
      - metadata # Metadata will tell the node that it's an Anvil
...
```

The yaml file is already configured for the correct deployment.


To give some context to the below commands, here's the directory structure that we've laid out. Yours will be different, so adjust accordingly:

NOTE: *This was being installed on an AMD host, so you will not need the `topoext` added if you're on an Intel platform. It's also worth noting that there may be other optimizations available, depending on your target platform, so please research accordingly.*


```shell
[~/Hammerspace]$ tree
.
├── hs-anvil-1
│   ├── config-drive.img
│   ├── data0.img
│   ├── hammerspace-5.1.22-296.qcow2
│   └── installer.yaml
├── hs-anvil-2
│   ├── config-drive.img
│   ├── data1.img
│   ├── hammerspace-5.1.22-296.qcow2
│   └── installer.yaml
├── hs-dsx-1
│   ├── config-drive.img
│   ├── data2.img
│   ├── hammerspace-5.1.22-296.qcow2
│   └── installer.yaml
└── hs-dsx-2
    ├── config-drive.img
    ├── data3.img
    ├── hammerspace-5.1.22-296.qcow2
    └── installer.yaml

```


For hs-anvil-1, we'll use the following `virt-install` command, but keep in mind that if you're doing this often, or your customer requires something more robust, you can use `xml templates` or you can use `terraform/openTofu`.


```shell
sudo virt-install  --name hs-anvil-1  --vcpus 8  --memory 16384  \
--cpu host,+topoext  --os-variant centos8  \--import \
--disk path=./hammerspace-5.1.22-296.qcow2,format=qcow2,bus=virtio  \
--disk path=./hs-anvil-1/config-drive.img,format=raw,bus=virtio  \
--disk path=./hs-anvil-1/data0.img,format=raw,bus=virtio \
--network network=default,model=virtio \
--graphics vnc,listen=0.0.0.0  \
--console pty,target_type=serial \
--video vga
```



For hs-anvil-2:

```shell
sudo virt-install  --name hs-anvil-2  --vcpus 8  --memory 16384  \
--cpu host,+topoext  --os-variant centos8  \--import \
--disk path=./hammerspace-5.1.22-296.qcow2,format=qcow2,bus=virtio  \
--disk path=./hs-anvil-2/config-drive.img,format=raw,bus=virtio  \
--disk path=./hs-anvil-2/data1.img,format=raw,bus=virtio \
--network network=default,model=virtio \
--graphics vnc,listen=0.0.0.0  \
--console pty,target_type=serial \
--video vga
```



For hs-dsx-1:

```shell

sudo virt-install  --name hs-dsx-1  --vcpus 4  --memory 8192  \
--cpu host,+topoext  --os-variant centos8  \--import \
--disk path=./hs-dsx-1/hammerspace-5.1.22-296.qcow2,format=qcow2,bus=virtio  \
--disk path=./hs-dsx-1/config-drive.img,format=raw,bus=virtio  \
--disk path=./hs-dsx-1/data2.img,format=raw,bus=virtio \
--network network=default,model=virtio \
--graphics vnc,listen=0.0.0.0  \
--console pty,target_type=serial \
--video vga
```

## Configure the Hammerspace Cluster

You should now be able to log into the Cluster. Navigate to:
`https://your-cluster-ip-address:8443`

From here, please refer to the Hammerspace User and Administration guide.
