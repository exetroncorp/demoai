#!/bin/bash

echo "############################################################"
echo "### 🧪 STARTING UML WORKAROUND TEST"
echo "############################################################"
echo ""
echo "--- We are 'root' inside a normal Docker container."
echo "--- User namespaces are ENABLED by default here."
echo "--- Testing 'podman' (rootless-style):"
echo ""

unshare -r echo "✅ SUCCESS: 'unshare -r' works. This container is not restricted."
echo ""
echo "------------------------------------------------------------"
echo "### 🚫 SIMULATING YOUR RESTRICTED HOST"
echo "------------------------------------------------------------"
echo "--- Now, disabling user namespaces to match your host..."
echo 0 > /proc/sys/user/max_user_namespaces
echo ""
echo "--- Re-testing 'unshare -r':"
unshare -r echo "This should not appear" 2>/dev/null || \
    echo "❌ FAILED: 'unshare -r' returned 'Operation not permitted'. We have successfully simulated your host!"
echo ""
echo "--- Attempting to run 'podman run' will now also fail."
echo ""
echo "------------------------------------------------------------"
echo "### 🚀 TESTING THE USER-MODE LINUX (UML) WORKAROUND"
echo "------------------------------------------------------------"
echo "--- We will now boot a FULL Linux kernel (UML) as a"
echo "--- single, unprivileged process using hostfs."
echo "--- This process does NOT need 'unshare' from the host."
echo ""
echo "--- Starting slirp4netns in BESS mode..."
echo ""

# Step 1: Start slirp4netns as a BESS server in the background
slirp4netns --target-type=bess /tmp/bess.sock &
SLIRP_PID=$!

# Give it a moment to initialize
sleep 2

echo "--- slirp4netns BESS server started (PID: $SLIRP_PID)"
echo "--- Now booting UML kernel with hostfs root and BESS networking..."
echo "--- (This uses the directory at /uml-root as the root filesystem)"
echo ""

# Create temp directory for UML (avoid /dev/shm noexec issues)
mkdir -p /tmp/uml-tmp

# Step 2: Start UML using hostfs as root filesystem
# This is MUCH simpler than trying to use disk images!
TMPDIR=/tmp/uml-tmp /linux-uml \
    vec0:transport=bess,dst=/tmp/bess.sock,depth=128,gro=1 \
    rootfstype=hostfs \
    hostfs=/uml-root \
    mem=1G \
    init=/bin/bash \
    rw

echo ""
echo "############################################################"
echo "### 🏁 UML KERNEL HAS EXITED"
echo "############################################################"

# Cleanup
kill $SLIRP_PID 2>/dev/null

echo ""
echo "After UML boots and you get a bash prompt, run these commands:"
echo ""
echo "  # Mount proc and sys"
echo "  mount -t proc proc /proc"
echo "  mount -t sysfs sys /sys"
echo ""
echo "  # Configure networking"
echo "  ip addr add 10.0.2.100/24 dev vec0"
echo "  ip link set vec0 up"
echo "  ip route add default via 10.0.2.2"
echo "  echo 'nameserver 10.0.2.3' > /etc/resolv.conf"
echo ""
echo "  # Test it!"
echo "  ping -c 3 10.0.2.2"
echo "  curl google.com"
echo "  podman run hello-world"
echo ""