import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class ControlCenterHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            status = {
                "active_agents": ["CEO", "Architect", "Coding", "QA", "Harvester"],
                "running_tasks": 3,
                "completed_tasks": 142,
                "system_health": "100%",
                "model_allocation": {
                    "Claude Opus 4.8": "25%",
                    "Claude Sonnet 4.6": "45%",
                    "Gemini 3.6 Flash": "20%",
                    "DeepSeek R1": "10%"
                },
                "total_cost_usd": 0.42,
                "git_commit": "79a11e2"
            }
            self.wfile.write(json.dumps(status).encode())
        else:
            # Serve frontend static files
            frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
            self.directory = frontend_dir
            super().do_GET()

def run_server(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ControlCenterHandler)
    print(f"Genesis Control Center running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
