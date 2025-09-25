#!/usr/bin/env bash
set -e

# Rust version & target
RUST_VERSION="1.90.0"
TARGET_TRIPLE="x86_64-unknown-linux-gnu"

ARCHIVE_NAME="rust-${RUST_VERSION}-${TARGET_TRIPLE}.tar.xz"
ARCHIVE_URL="https://static.rust-lang.org/dist/${ARCHIVE_NAME}"

# Writable directories
DOWNLOAD_DIR="${HOME}/downloads"
INSTALL_DIR="${HOME}/.local/rust-${RUST_VERSION}"
TMPDIR="${HOME}/tmp-rust-install"

# Create dirs
mkdir -p "${DOWNLOAD_DIR}"
mkdir -p "$(dirname "${INSTALL_DIR}")"

# Download
echo "==> Downloading ${ARCHIVE_URL}"
wget -O "${DOWNLOAD_DIR}/${ARCHIVE_NAME}" "${ARCHIVE_URL}"

# Extract
rm -rf "${TMPDIR}"
mkdir -p "${TMPDIR}"
tar -xf "${DOWNLOAD_DIR}/${ARCHIVE_NAME}" -C "${TMPDIR}"

# Move install
UNPACKED_DIR="${TMPDIR}/rust-${RUST_VERSION}-${TARGET_TRIPLE}"
mv "${UNPACKED_DIR}" "${INSTALL_DIR}"

# Cleanup
rm -rf "${TMPDIR}"

echo ""
echo "=== Rust ${RUST_VERSION} installed locally at ${INSTALL_DIR} ==="
echo ""
echo "Add this to your ~/.bashrc or ~/.profile:"
echo "  export RUST_HOME=\"${INSTALL_DIR}\""
echo "  export PATH=\"\$RUST_HOME/bin:\$PATH\""
echo ""
echo "Then run: source ~/.bashrc"
echo "Check with:"
echo "  rustc --version"
echo "  cargo --version"
