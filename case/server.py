
import http.server
import json
import os

PORT = 8765
BASE = '/Users/jowos/code/sofle-procyon'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE, **kwargs)

    def do_GET(self):
        if self.path == '/case/pcb_data.json' or self.path == '/pcb_data.json':
            # Always serve fresh data from disk
            data_path = os.path.join(BASE, 'case/pcb_data.json')
            with open(data_path) as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/save':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            with open(os.path.join(BASE, 'case/pcb_data.json'), 'w') as f:
                json.dump(data, f, indent=2)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Saved to case/pcb_data.json')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress logs

print(f"PCB Annotator running at http://localhost:{PORT}/case/annotator.html")
print("Press Ctrl+C to stop")
http.server.HTTPServer(('', PORT), Handler).serve_forever()
