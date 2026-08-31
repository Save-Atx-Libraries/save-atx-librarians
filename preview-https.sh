#!/bin/bash
# LAN HTTPS preview for SOLATX. Uses a self-signed cert (no public CA will
# sign a 192.168.x address). Does not push anything.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
IP="${PREVIEW_IP:-192.168.1.189}"
CERT_DIR=".preview-tls"
URL="https://${IP}:${PORT}/"

mkdir -p "$CERT_DIR"
if [[ ! -f "$CERT_DIR/cert.pem" || ! -f "$CERT_DIR/key.pem" ]]; then
  echo "Making a self-signed cert for ${IP}, 127.0.0.1, localhost"
  openssl req -x509 -newkey rsa:2048 -sha256 -days 825 -nodes \
    -keyout "$CERT_DIR/key.pem" \
    -out "$CERT_DIR/cert.pem" \
    -subj "/CN=solatx-preview" \
    -addext "subjectAltName=IP:${IP},IP:127.0.0.1,DNS:localhost"
  chmod 600 "$CERT_DIR/key.pem"
fi

if command -v ss >/dev/null 2>&1 && ss -tln | grep -q ":${PORT} "; then
  echo "Port ${PORT} is already in use."
  echo "If the old HTTP preview is still up, stop it, then run this again."
  echo "Then open ${URL}"
  exit 1
fi

echo "SOLATX HTTPS preview → ${URL}"
echo "Browser will say the cert is not trusted. Advanced → proceed / accept."
HOST="$HOST" PORT="$PORT" python3 tools/https_preview.py
