#!/usr/bin/env python3
"""Serve the Meet Memory build on http://localhost only (never on the network).

Uses only the Python standard library. The cross-origin-isolation headers let Whisper's
WebAssembly backend use several CPU threads; the CSP header repeats the page's own policy.
"""
import functools
import http.server
import os
import subprocess
import sys
import threading

HOST = "127.0.0.1"
PORT = int(os.environ.get("MEET_MEMORY_PORT", "8765"))
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
if not os.path.isdir(ROOT):
    ROOT = os.path.dirname(os.path.abspath(__file__))  # running from the build output itself


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".wasm": "application/wasm",
        ".mjs": "text/javascript",
        ".js": "text/javascript",
        ".onnx": "application/octet-stream",
        ".json": "application/json",
        ".svg": "image/svg+xml",
    }

    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):  # keep the terminal quiet
        pass


def open_chrome(url):
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", "-a", "Google Chrome", url], check=True)
        else:
            raise OSError
    except Exception:
        print(f"Open this address in Google Chrome: {url}")


def main():
    handler = functools.partial(Handler, directory=ROOT)
    try:
        server = http.server.ThreadingHTTPServer((HOST, PORT), handler)
    except OSError as error:
        sys.exit(f"Could not start on port {PORT}: {error}\nSet MEET_MEMORY_PORT to another number and retry.")
    url = f"http://localhost:{PORT}/"
    print(f"Meet Memory is running at {url}\nKeep this window open while you use it. Press Ctrl+C to stop.")
    threading.Timer(0.8, open_chrome, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
