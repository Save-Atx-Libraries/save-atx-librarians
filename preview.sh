#!/bin/bash
# Local preview for SOLATX. Does not push anything.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-8080}"
URL="http://127.0.0.1:${PORT}/"

if command -v ss >/dev/null 2>&1 && ss -tln | grep -q ":${PORT} "; then
  echo "Already serving on ${URL}"
else
  echo "SOLATX local preview → ${URL}"
  echo "This is only on this computer. Close this window to stop the server."
  python3 -m http.server "$PORT" --bind 127.0.0.1 &
  PREVIEW_PID=$!
  trap 'kill "$PREVIEW_PID" 2>/dev/null || true' EXIT
  sleep 0.4
fi

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 || true
elif command -v firefox >/dev/null 2>&1; then
  firefox "$URL" >/dev/null 2>&1 || true
fi

if [[ -n "${PREVIEW_PID:-}" ]]; then
  wait "$PREVIEW_PID"
fi
