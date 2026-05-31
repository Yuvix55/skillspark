from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, json, os

GROQ_KEY = os.environ.get("GROQ_KEY", "")
PORT = int(os.environ.get("PORT", 8787))

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps({"status": "SkillSpark server live hai!"}).encode())

    def do_POST(self):
        if self.path != '/groq':
            self.send_response(404)
            self.end_headers()
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {GROQ_KEY}'
            }
            req = urllib.request.Request(
                'https://api.groq.com/openai/v1/chat/completions',
                data=body, headers=headers, method='POST'
            )
            with urllib.request.urlopen(req) as r:
                resp = r.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(resp)
        except urllib.error.HTTPError as e:
            err = e.read()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(err)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

print(f"SkillSpark Server port {PORT} pe chal raha hai!")
server = HTTPServer(('0.0.0.0', PORT), Handler)
server.serve_forever()
