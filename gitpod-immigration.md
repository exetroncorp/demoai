# syntax=docker/dockerfile:experimental

ARG BASE=debian:12
FROM $BASE

# ADDED: Argument for OpenVSCode Server version for easier updates.
# Find the latest version at: https://github.com/gitpod-io/openvscode-server/releases
ARG OPENVSCODE_SERVER_VERSION=v1.90.1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    curl \
    dumb-init \
    git \
    git-lfs \
    htop \
    locales \
    lsb-release \
    man-db \
    nano \
    openssh-client \
    procps \
    sudo \
    vim-tiny \
    wget \
    zsh \
    # ADDED: libatomic1 is a dependency for openvscode-server
    libatomic1 \
  && git lfs install \
  && rm -rf /var/lib/apt/lists/*

# https://wiki.debian.org/Locale#Manually
RUN sed -i "s/# en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen \
  && locale-gen
ENV LANG=en_US.UTF-8

# This section remains the same to preserve your user structure.
RUN if grep -q 1000 /etc/passwd; then \
    userdel -r "$(id -un 1000)"; \
  fi \
  && adduser --gecos '' --disabled-password coder \
  && echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd

# This section remains the same to preserve your fixuid logic.
RUN ARCH="$(dpkg --print-architecture)" \
  && curl -fsSL "https://github.com/boxboat/fixuid/releases/download/v0.6.0/fixuid-0.6.0-linux-$ARCH.tar.gz" | tar -C /usr/local/bin -xzf - \
  && chown root:root /usr/local/bin/fixuid \
  && chmod 4755 /usr/local/bin/fixuid \
  && mkdir -p /etc/fixuid \
  && printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

# --- MODIFIED: Installation of OpenVSCode Server ---
# This block replaces the debian package installation for code-server.
RUN ARCH="$(dpkg --print-architecture)" \
  && case "${ARCH}" in \
    amd64) ARCH_ALIAS="x64";; \
    arm64) ARCH_ALIAS="arm64";; \
    *) echo "Unsupported architecture: ${ARCH}"; exit 1;; \
  esac \
  # Using /opt/ is a standard location for optional software.
  && mkdir -p /opt/openvscode-server \
  && curl -fsSL "https://github.com/gitpod-io/openvscode-server/releases/download/openvscode-server-${OPENVSCODE_SERVER_VERSION}/openvscode-server-${OPENVSCODE_SERVER_VERSION}-linux-${ARCH_ALIAS}.tar.gz" \
  | tar -C /opt/openvscode-server --strip-components=1 -xzf - \
  && chown -R coder:coder /opt/openvscode-server
# --- End of MODIFIED section ---

# You are keeping your custom entrypoint script.
# You MUST modify this script to call the new executable. See notes below.
COPY ci/release-image/entrypoint.sh /usr/bin/entrypoint.sh

# This line is removed as we are no longer using a multi-stage build for packages.
# RUN --mount=from=packages,src=/tmp,dst=/tmp/packages dpkg -i /tmp/packages/code-server*$(dpkg --print-architecture).deb

# Allow users to have scripts run on container startup to prepare workspace.
# https://github.com/coder/code-server/issues/5177
ENV ENTRYPOINTD=${HOME}/entrypoint.d

EXPOSE 8080

# This user setup remains the same, which is critical for your logic.
USER 1000
ENV USER=coder
WORKDIR /home/coder

# The entrypoint command remains the same, as it calls your custom script.
# The logic inside entrypoint.sh needs to be changed.
ENTRYPOINT ["/usr/bin/entrypoint.sh", "--host", "0.0.0.0", "--port", "8080"]



------------------------------------------------



# Modify the last line of your entrypoint.sh to this
# The new executable is at /opt/openvscode-server/bin/openvscode-server
# --without-connection-token is recommended for this kind of setup.
exec dumb-init /opt/openvscode-server/bin/openvscode-server --without-connection-token "$@"
