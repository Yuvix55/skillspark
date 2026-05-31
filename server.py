from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, json, os

GROQ_KEY = os.environ.get("GROQ_KEY", "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")
PORT     = int(os.environ.get("PORT", 8787))

ROUTES = {
    '/groq': ('https://api.groq.com/openai/v1/chat/completions', {
                  'Content-Type':  'application/json',
                  'Authorization': f'Bearer {GROQ_KEY}'
              }),
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

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
        if self.path not in ROUTES:
            self.send_response(404); self.end_headers(); return
        target_url, headers = ROUTES[self.path]
        try:
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            req    = urllib.request.Request(target_url, data=body,
                                            headers=headers, method='POST')
            with urllib.request.urlopen(req) as r:
                resp = r.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._cors(); self.end_headers()
            self.wfile.write(resp)
        except urllib.error.HTTPError as e:
            err = e.read()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._cors(); self.end_headers()
            self.wfile.write(err)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._cors(); self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

print(f"SkillSpark Server chal raha hai port {PORT} pe!")
server = HTTPServer(('0.0.0.0', PORT), Handler)
server.serve_forever()
