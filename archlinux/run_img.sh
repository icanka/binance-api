#!/bin/sh
# For more information on qemu other than detailed documentation, visit: 
# 'https://wiki.archlinux.org/title/QEMU'
# 'https://cloudinit.readthedocs.io/en/22.4.2/topics/datasources.html'
# 'https://cloudinit.readthedocs.io/en/latest/topics/datasources/nocloud.html'

##############################################QUICK COMMAND NOTES############################################################
# Run qcow2 image with 2 gigs of ram and use kvm for hardware assisted virtualization.
# $ qemu-system-x86_64 -accel kvm -m 2G Arch-Linux-x86_64-cloudimg.qcow2
# create an overlay image
# $ qemu-img create -o backing_file=Arch-Linux-x86_64-cloudimg.qcow2,backing_fmt=qcow2 -f qcow2 img1.cow
##############################################QUICK COMMAND NOTES############################################################

export SSHPASS=passw0rd

# Datasources are sources of configuration data for cloud-init that typically come from the user (i.e. userdata) or 
# come from the cloud that created the configuration drive (i.e. metadata). Typical userdata would include files, YAML, 
# and shell scripts while typical metadata would include server name, instance id, display name and other cloud specific details.
# Since there are multiple ways to provide this data (each cloud solution seems to prefer its own way) internally a 
# datasource abstract class was created to allow for a single way to access the different cloud systems methods to provide 
# this data through the typical usage of subclasses. Any metadata processed by cloud-init’s datasources is 
# persisted as /run/cloud-init/instance-data.json.

# The data source NoCloud allows the user to provide user-data and meta-data to the instance without running a network service 
# (or even without having a network at all).You can provide meta-data and user-data to a local vm boot via files
# on a vfat or iso9660 filesystem. The filesystem volume label must be cidata or CIDATA.

# The data source NoCloud allows the user to provide user-data and meta-data to the instance without
# running a network service (or even without having a network at all).
# You can provide meta-data and user-data to a local vm boot via files on a vfat or iso9660 filesystem.
# The filesystem volume label must be cidata or CIDATA.

# cloud-init config required to enable ssh.
cat >user-data <<EOF
#cloud-config
password: '${SSHPASS}'
chpasswd: { expire: False }
ssh_pwauth: True
packages:
  - tmux
  - tree
runcmd:
  - [ echo, 'Install more packages using runcmd.' ]
  - [ pacman, --noconfirm, -Syu, bat ]
  - [ touch, /runcmd_successful ]
EOF

cat >meta-data <<EOF
instance-id: iid-local01
local-hostname: cloudimg
EOF
cat user-data meta-data

# Create an iso with the files we have created
genisoimage -output seed.iso -volid cidata -joliet -rock user-data meta-data

#  QEMU offers guests the ability to use paravirtualized block and network devices using the virtio drivers,
#  which provide better performance and lower overhead.
#  A virtio block device requires the option -drive for passing a disk image, with parameter if=virtio
#  Virtio is a virtualization standard for network and disk device drivers where just the guest's device driver
#  "knows" it is running in a virtual environment, and cooperates with the hypervisor. This enables guests to
#  get high performance network and disk operations, and gives most of the performance benefits of paravirtualization.
#  Note: This will only work if the guest machine has drivers for virtio devices. Linux does, and the required drivers are included
#  in Arch Linux, but there is no guarantee that virtio devices will work with other operating systems.
# Note: '-accel kvm' option makes a huge difference in speed.

# Run the image with iso mounted
nohup qemu-system-x86_64 -accel kvm -m 512 -net nic -net user,hostfwd=tcp::2222-:22 -monitor telnet:127.0.0.1:55555,server,nowait \
  -drive file=$(ls arch-boxes/output/Arch-Linux-x86_64-cloudimg-*.qcow2),if=virtio -drive file=seed.iso,if=virtio -nographic &
# now you can ssh into the qemu virt. machine as: 'ssh arch@localhost -p 2222'
# and you can connect to listening qemu monitor to control the virtual machine with telnet as: 'telnet 127.0.0.1 55555'

# Some operations of a physical machine can be emulated by QEMU using some monitor commands:
#  'system_powerdown' will send an ACPI shutdown request to the virtual machine. This effect is similar to the power button in a physical machine.
#  'system_reset' will reset the virtual machine similarly to a reset button in a physical machine. This operation can cause data loss and file system corruption since the virtual machine is not cleanly restarted.
#  'stop' will pause the virtual machine.
#  'cont' will resume a virtual machine previously paused.

# Inspect the boot process
timeout 1m sh -c 'tail -f nohup.out' &

# Log in to the machine.
until sshpass -e ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no arch@localhost -p 2222
do sleep 3;done

# timeout 15m sh -c "while ! sshpass -e ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no arch@localhost -p 2222 true; do sleep 1; done"
# timeout 15m sh -c "while ! sshpass -e ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no arch@localhost -p 2222 pacman -Q bat tmux tree; do sleep 1; done"
# timeout 15m sh -c "while ! sshpass -e ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no arch@localhost -p 2222 test -f /runcmd_successful ; do sleep 1; done"
