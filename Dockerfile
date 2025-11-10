# Use Debian 12 (bookworm) as our base
FROM debian:12

# Set non-interactive to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install all necessary tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    user-mode-linux \
    debootstrap \
    slirp4netns \
    podman \
    curl \
    ca-certificates \
    dos2unix \
    && apt-get clean

# 2. Create a directory for the guest OS
RUN mkdir -p /uml-root

# 3. Bootstrap a minimal Debian 12 system
RUN debootstrap --variant=minbase bookworm /uml-root http://deb.debian.org/debian

# 4. Install podman and other tools inside the guest
RUN chroot /uml-root apt-get update && \
    chroot /uml-root apt-get install -y --no-install-recommends \
        podman \
        nano \
        iproute2 \
        iputils-ping \
        curl \
        ca-certificates \
    && chroot /uml-root apt-get clean

# 5. Set root password to 'root'
RUN chroot /uml-root sh -c 'echo "root:root" | chpasswd'

# 6. Copy the UML kernel
RUN cp /usr/bin/linux /linux-uml

# 7. Copy the test script
COPY run-test.sh /run-test.sh
RUN dos2unix /run-test.sh && chmod +x /run-test.sh

# The default command
CMD ["/run-test.sh"]