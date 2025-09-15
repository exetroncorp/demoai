FROM debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    TZ=Etc/UTC \
    XPRA_HTML_PORT=10000 \
    DISPLAY=:100 \
    USER_NAME=dev \
    USER_UID=1000 \
    USER_GID=1000 \
    XDG_RUNTIME_DIR=/run/user/1000

# Install base system tools and desktop environment
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl wget gnupg xz-utils sudo dbus-x11 \
    xserver-xorg-video-dummy xauth \
    openbox pcmanfm lxterminal \
    fonts-dejavu feh libgl1-mesa-dri libjs-jquery \
    && rm -rf /var/lib/apt/lists/*

# Add Xpra APT source using modern .sources format
RUN curl -fsSL https://xpra.org/xpra.asc | tee /usr/share/keyrings/xpra.asc > /dev/null && \
    echo "Types: deb" > /etc/apt/sources.list.d/xpra.sources && \
    echo "URIs: https://xpra.org" >> /etc/apt/sources.list.d/xpra.sources && \
    echo "Suites: bookworm" >> /etc/apt/sources.list.d/xpra.sources && \
    echo "Components: main" >> /etc/apt/sources.list.d/xpra.sources && \
    echo "Signed-By: /usr/share/keyrings/xpra.asc" >> /etc/apt/sources.list.d/xpra.sources && \
    echo "Architectures: amd64 arm64" >> /etc/apt/sources.list.d/xpra.sources && \
    apt-get update && \
    apt-get install -y xpra && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and runtime directories
RUN groupadd -g ${USER_GID} ${USER_NAME} && \
    useradd -m -u ${USER_UID} -g ${USER_GID} -s /bin/bash ${USER_NAME} && \
    echo "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-${USER_NAME} && \
    mkdir -p /run/user/${USER_UID}/xpra /run/xpra /tmp/.X11-unix && \
    chown -R ${USER_NAME}:${USER_NAME} /run/user/${USER_UID} /run/xpra && \
    chmod 755 /run/user/${USER_UID} && \
    chmod 1777 /tmp/.X11-unix

USER ${USER_NAME}
WORKDIR /home/${USER_NAME}

# Download wallpaper
RUN wget -q "https://w0.peakpx.com/wallpaper/304/561/HD-wallpaper-streets-of-rage-4-bare-knuckle-streets-of-rage-4-2020-games-games.jpg" \
    -O /home/${USER_NAME}/wallpaper.jpg

# Openbox autostart configuration
RUN mkdir -p .config/openbox && \
    echo '#!/bin/bash' > .config/openbox/autostart && \
    echo '(feh --bg-scale ~/wallpaper.jpg) &' >> .config/openbox/autostart && \
    echo '(sleep 2 && pcmanfm --desktop --profile LXDE) &' >> .config/openbox/autostart && \
    chmod +x .config/openbox/autostart

# Xpra startup script
RUN echo '#!/usr/bin/env bash' > start.sh && \
    echo 'set -exo pipefail' >> start.sh && \
    echo 'mkdir -p "$XDG_RUNTIME_DIR/xpra"' >> start.sh && \
    echo 'if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then' >> start.sh && \
    echo '  eval $(dbus-launch --sh-syntax)' >> start.sh && \
    echo 'fi' >> start.sh && \
    echo 'exec xpra start-desktop :100 \' >> start.sh && \
    echo '  --start-child="openbox-session" \' >> start.sh && \
    echo '  --bind-tcp=0.0.0.0:$XPRA_HTML_PORT \' >> start.sh && \
    echo '  --html=on \' >> start.sh && \
    echo '  --tcp-auth=none \' >> start.sh && \
    echo '  --exit-with-children=yes \' >> start.sh && \
    echo '  --video-encoder=x264 \' >> start.sh && \
    echo '  --encoding=rgb \' >> start.sh && \
    echo '  --quality=60 --min-quality=30 \' >> start.sh && \
    echo '  --speed=90 --min-speed=50 \' >> start.sh && \
    echo '  --opengl=no \' >> start.sh && \
    echo '  --speaker=off --microphone=off --webcam=no --printing=no \' >> start.sh && \
    echo '  --mdns=no \' >> start.sh && \
    echo '  --notifications=no \' >> start.sh && \
    echo '  --window-close=disconnect \' >> start.sh && \
    echo '  --daemon=no' >> start.sh && \
    chmod +x start.sh

EXPOSE 10000/tcp

ENTRYPOINT ["./start.sh"]
