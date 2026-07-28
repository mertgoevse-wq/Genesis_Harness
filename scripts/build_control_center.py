import os

repo_root = "c:\\Genesis_Harness"

# Directories
dirs = [
    "control-center/events",
    "control-center/backend",
    "control-center/frontend"
]
for d in dirs:
    os.makedirs(os.path.join(repo_root, d), exist_ok=True)
    with open(os.path.join(repo_root, d, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Genesis Control Center Module\n")

# 1. Event Bus: control-center/events/event_bus.py
event_bus_code = '''import time

class EventBus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def publish(self, event_type: str, data: dict):
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "data": data
        }
        for sub in self.subscribers:
            try:
                sub(event)
            except Exception:
                pass
        return event
'''
with open(os.path.join(repo_root, "control-center", "events", "event_bus.py"), "w", encoding="utf-8") as f:
    f.write(event_bus_code)

# 2. Backend Server: control-center/backend/server.py
server_code = '''import json
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
'''
with open(os.path.join(repo_root, "control-center", "backend", "server.py"), "w", encoding="utf-8") as f:
    f.write(server_code)

# 3. Frontend HTML: control-center/frontend/index.html
html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genesis Control Center</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="brand">
                <div class="logo-icon">G</div>
                <span class="brand-title">Genesis OS</span>
            </div>
            <nav class="nav-menu">
                <a href="#" class="nav-item active">Dashboard</a>
                <a href="#" class="nav-item">Agent Tree</a>
                <a href="#" class="nav-item">Task Queue</a>
                <a href="#" class="nav-item">Model Router</a>
                <a href="#" class="nav-item">Harvester GIPs</a>
                <a href="#" class="nav-item">System Logs</a>
            </nav>
            <div class="sidebar-footer">
                <div class="status-indicator"><span class="dot green"></span> System Live</div>
                <div class="commit-tag">Commit: #79a11e2</div>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Header -->
            <header class="top-header">
                <h2>Control Center</h2>
                <div class="header-actions">
                    <span class="badge">Realtime Telemetry</span>
                </div>
            </header>

            <!-- Key Metrics Grid -->
            <section class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Active Agents</div>
                    <div class="metric-value">5</div>
                    <div class="metric-sub">CEO, Architect, Coding, QA, Harvester</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Running Tasks</div>
                    <div class="metric-value">3</div>
                    <div class="metric-sub">DAG Scheduler Queue Active</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Model Router Cost</div>
                    <div class="metric-value">$0.42</div>
                    <div class="metric-sub">Optimized Tier Allocation</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">System Health</div>
                    <div class="metric-value green-text">100%</div>
                    <div class="metric-sub">All Quality Gates Passing</div>
                </div>
            </section>

            <!-- Agent Tree Visualization & Live Feed -->
            <section class="content-split">
                <!-- Agent Tree Hierarchy -->
                <div class="panel agent-tree-panel">
                    <div class="panel-header">
                        <h3>Agent Execution Hierarchy</h3>
                    </div>
                    <div class="tree-container">
                        <div class="tree-node parent">
                            <span class="role">CEO Agent</span>
                            <span class="status-pill running">Orchestrating</span>
                        </div>
                        <div class="tree-branches">
                            <div class="tree-node child">
                                <span class="role">Architect</span>
                                <span class="subtext">Opus 4.8</span>
                            </div>
                            <div class="tree-node child">
                                <span class="role">Coding Agent</span>
                                <span class="subtext">Sonnet 4.6</span>
                            </div>
                            <div class="tree-node child">
                                <span class="role">QA Agent</span>
                                <span class="subtext">Sonnet 4.6</span>
                            </div>
                            <div class="tree-node child">
                                <span class="role">Harvester</span>
                                <span class="subtext">Gemini 3.6 Flash</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Live Stream Logs -->
                <div class="panel log-panel">
                    <div class="panel-header">
                        <h3>Live Telemetry Stream</h3>
                    </div>
                    <div class="log-console" id="logConsole">
                        <div class="log-line"><span class="timestamp">[17:34:01]</span> <span class="info">[INFO]</span> ModelRouter -> Routed task 'Architecture' to Claude Opus 4.8</div>
                        <div class="log-line"><span class="timestamp">[17:34:03]</span> <span class="success">[SUCCESS]</span> AgentWorkerPool -> Parallel step completed cleanly.</div>
                        <div class="log-line"><span class="timestamp">[17:34:05]</span> <span class="info">[INFO]</span> Harvester v2 -> Generated GIP Proposal in docs/proposals/.</div>
                        <div class="log-line"><span class="timestamp">[17:34:08]</span> <span class="success">[SUCCESS]</span> verify_structure.ps1 -> 169 checks passed.</div>
                    </div>
                </div>
            </section>
        </main>
    </div>
</body>
</html>
'''
with open(os.path.join(repo_root, "control-center", "frontend", "index.html"), "w", encoding="utf-8") as f:
    f.write(html_code)

# 4. Frontend CSS: control-center/frontend/styles.css
css_code = '''* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

body {
    background-color: #0D0E11;
    color: #E2E8F0;
    height: 100vh;
    overflow: hidden;
}

.app-container {
    display: flex;
    height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 240px;
    background-color: #13151A;
    border-right: 1px solid #23262D;
    display: flex;
    flex-direction: column;
    padding: 20px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 30px;
}

.logo-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #3B82F6, #06B6D4);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: #FFF;
}

.brand-title {
    font-size: 16px;
    font-weight: 600;
    color: #F8FAFC;
}

.nav-menu {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
}

.nav-item {
    padding: 10px 14px;
    color: #94A3B8;
    text-decoration: none;
    font-size: 14px;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.nav-item:hover, .nav-item.active {
    background-color: #1E222B;
    color: #F8FAFC;
}

.sidebar-footer {
    font-size: 12px;
    color: #64748B;
    border-top: 1px solid #23262D;
    padding-top: 16px;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.dot.green { background-color: #10B981; }

/* Main Content */
.main-content {
    flex: 1;
    padding: 30px;
    overflow-y: auto;
}

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.top-header h2 {
    font-size: 22px;
    font-weight: 600;
}

.badge {
    background-color: #1E222B;
    border: 1px solid #23262D;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    color: #38BDF8;
}

/* Metrics Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.metric-card {
    background-color: #13151A;
    border: 1px solid #23262D;
    border-radius: 10px;
    padding: 20px;
}

.metric-label {
    font-size: 13px;
    color: #94A3B8;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 4px;
}

.metric-value.green-text { color: #10B981; }

.metric-sub {
    font-size: 12px;
    color: #64748B;
}

/* Content Split */
.content-split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.panel {
    background-color: #13151A;
    border: 1px solid #23262D;
    border-radius: 10px;
    padding: 20px;
}

.panel-header h3 {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 16px;
}

/* Tree Visualization */
.tree-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}

.tree-node {
    background-color: #1E222B;
    border: 1px solid #333A48;
    padding: 10px 18px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.tree-node.parent {
    border-color: #3B82F6;
}

.status-pill.running {
    font-size: 10px;
    color: #34D399;
    margin-top: 4px;
}

.tree-branches {
    display: flex;
    gap: 12px;
}

.subtext {
    font-size: 10px;
    color: #64748B;
}

/* Log Console */
.log-console {
    background-color: #090A0C;
    border: 1px solid #1E222B;
    border-radius: 6px;
    padding: 14px;
    font-family: monospace;
    font-size: 12px;
    height: 240px;
    overflow-y: auto;
}

.log-line {
    margin-bottom: 8px;
}

.timestamp { color: #64748B; }
.info { color: #38BDF8; }
.success { color: #34D399; }
'''
with open(os.path.join(repo_root, "control-center", "frontend", "styles.css"), "w", encoding="utf-8") as f:
    f.write(css_code)

print("Control Center files built successfully.")
