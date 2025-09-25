#!/usr/bin/env bash
set -e

# ================
# Config variables
# ================

# Rust
RUST_VERSION="1.90.0"
RUST_TARGET="x86_64-unknown-linux-gnu"
RUST_ARCHIVE="rust-${RUST_VERSION}-${RUST_TARGET}.tar.xz"
RUST_URL="https://static.rust-lang.org/dist/${RUST_ARCHIVE}"
RUST_INSTALL_DIR="${HOME}/.local/rust-${RUST_VERSION}"

# RustRover
RR_VERSION="2025.2.2"
RR_ARCHIVE="RustRover-${RR_VERSION}.tar.gz"
RR_URL="https://download.jetbrains.com/rustrover/${RR_ARCHIVE}"
RR_INSTALL_DIR="${HOME}/RustRover-${RR_VERSION}"

# Writable dirs
DOWNLOAD_DIR="${HOME}/downloads"
TMPDIR="${HOME}/tmp-install"

# ================
# Prepare dirs
# ================
mkdir -p "${DOWNLOAD_DIR}"
rm -rf "${TMPDIR}"
mkdir -p "${TMPDIR}"

# ================
# Install Rust
# ================
echo "==> Downloading Rust ${RUST_VERSION}"
wget -O "${DOWNLOAD_DIR}/${RUST_ARCHIVE}" "${RUST_URL}"

echo "==> Extracting Rust"
tar -xf "${DOWNLOAD_DIR}/${RUST_ARCHIVE}" -C "${TMPDIR}"

UNPACKED_RUST="${TMPDIR}/rust-${RUST_VERSION}-${RUST_TARGET}"
rm -rf "${RUST_INSTALL_DIR}"
mv "${UNPACKED_RUST}" "${RUST_INSTALL_DIR}"

echo "==> Rust installed into ${RUST_INSTALL_DIR}"

# ================
# Install RustRover
# ================
echo "==> Downloading RustRover ${RR_VERSION}"
wget -O "${DOWNLOAD_DIR}/${RR_ARCHIVE}" "${RR_URL}"

echo "==> Extracting RustRover"
tar -xf "${DOWNLOAD_DIR}/${RR_ARCHIVE}" -C "${HOME}"

# Remove old if exists
rm -rf "${RR_INSTALL_DIR}"
mv "${HOME}/RustRover-${RR_VERSION}" "${RR_INSTALL_DIR}" || true

echo "==> RustRover installed into ${RR_INSTALL_DIR}"

# ================
# Cleanup
# ================
rm -rf "${TMPDIR}"

# ================
# Environment setup
# ================
echo ""
echo "=== Installation finished ==="
echo ""
echo "Add these lines to your ~/.bashrc or ~/.profile:"
echo ""
echo "  # Rust"
echo "  export RUST_HOME=\"${RUST_INSTALL_DIR}\""
echo "  export PATH=\"\$RUST_HOME/bin:\$PATH\""
echo ""
echo "  # RustRover"
echo "  export PATH=\"${RR_INSTALL_DIR}/bin:\$PATH\""
echo ""
echo "Then reload your shell (source ~/.bashrc)."
echo ""
echo "You can test with:"
echo "  rustc --version"
echo "  cargo --version"
echo "  rustrover.sh &   # to launch RustRover"
