#!/usr/bin/env python3
"""Serve the SOLATX folder over HTTPS on the LAN. Certs live in .preview-tls/."""
from __future__ import annotations

import os
import ssl
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / ".preview-tls"
CERT = CERT_DIR / "cert.pem"
KEY = CERT_DIR / "key.pem"


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".css": "text/css; charset=utf-8",
        ".html": "text/html; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
    }


def main() -> None:
    os.chdir(ROOT)
    if not CERT.is_file() or not KEY.is_file():
        raise SystemExit("Missing .preview-tls/cert.pem — run preview-https.sh first.")
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    httpd = ThreadingHTTPServer((host, port), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(CERT, KEY)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print(f"SOLATX HTTPS preview → https://192.168.1.189:{port}/")
    print("Self-signed cert. The browser will warn once; choose Advanced, then proceed.")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
