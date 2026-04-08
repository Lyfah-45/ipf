#!/usr/bin/env python3
"""
Gallery Server
Run with: python server.py
Then open: http://localhost:8000
Place your images inside the ./Images folder.
"""

import os
import json
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler

IMAGES_DIR = "Images"
SUPPORTED_EXTS = {
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp',
    '.tiff', '.tif', '.cr2', '.nef', '.raw', '.arw',
    '.dng', '.orf', '.rw2', '.pef'
}

class GalleryHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # API: return list of image files as JSON
        if self.path == "/api/images":
            self.serve_image_list()
        else:
            # Serve static files normally (index.html, Images/*, etc.)
            super().do_GET()

    def serve_image_list(self):
        images = []
        if os.path.isdir(IMAGES_DIR):
            for fname in sorted(os.listdir(IMAGES_DIR)):
                ext = os.path.splitext(fname)[1].lower()
                if ext in SUPPORTED_EXTS:
                    fpath = os.path.join(IMAGES_DIR, fname)
                    size = os.path.getsize(fpath)
                    images.append({
                        "name": fname,
                        "url": f"/Images/{fname}",
                        "size": size,
                        "ext": ext.lstrip('.')
                    })

        body = json.dumps(images).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Cleaner log output
        print(f"  {self.address_string()} → {args[0]}")

if __name__ == "__main__":
    port = 8000
    print(f"\n📷  Gallery Server")
    print(f"    Serving images from: ./{IMAGES_DIR}/")
    print(f"    Open in browser:     http://localhost:{port}\n")
    server = HTTPServer(("", port), GalleryHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
