#!/usr/bin/env python3
"""Serveur local Clartéo : IPv4 + IPv6, toutes interfaces, port 8000."""
from __future__ import annotations

import contextlib
import functools
import os
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("CLARTEO_PORT", "8000"))
ROOT = os.path.dirname(os.path.abspath(__file__))


class DualStackServer(ThreadingHTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True
    allow_reuse_address = True

    def server_bind(self) -> None:
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


def main() -> None:
    handler = functools.partial(SimpleHTTPRequestHandler, directory=ROOT)
    httpd = DualStackServer(("::", PORT), handler)
    print(f"Clartéo  http://127.0.0.1:{PORT}/", flush=True)
    print(f"         http://[::1]:{PORT}/", flush=True)
    print(f"Racine   {ROOT}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt.")


if __name__ == "__main__":
    main()
