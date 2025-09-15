#!/usr/bin/env bash
set -exo pipefail

mkdir -p "$XDG_RUNTIME_DIR/xpra"

if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then
  eval "$(dbus-launch --sh-syntax)"
fi

exec xpra start-desktop :100 \
  --start-child="openbox-session" \
  --bind-tcp=0.0.0.0:10000 \
  --html=on \
  --tcp-auth=none \
  --exit-with-children=yes \
  --video-encoder=x264 \
  --encoding=rgb \
  --quality=60 --min-quality=30 \
  --speed=90 --min-speed=50 \
  --opengl=no \
  --ping-interval=5 --ping-timeout=15 \
  --speaker=off --microphone=off --webcam=no --printing=no \
  --mdns=no --notifications=no \
  --window-close=disconnect \
  --debug=encoding,damage,screen,fps,stats \
  --daemon=no
