import os
import json

class DependencyAnalyzer:
    """Analyzes project dependencies."""
    
    def analyze(self, root_dir: str) -> dict:
        """Finds and lists dependencies from requirements.txt or package.json"""
        deps = {"python": [], "node": []}
        
        req_file = os.path.join(root_dir, "requirements.txt")
        if os.path.exists(req_file):
            with open(req_file, 'r', encoding='utf-8') as f:
                deps["python"] = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
        pkg_file = os.path.join(root_dir, "package.json")
        if os.path.exists(pkg_file):
            with open(pkg_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    deps["node"] = list(data.get("dependencies", {}).keys())
                except json.JSONDecodeError:
                    pass
                    
        return deps
