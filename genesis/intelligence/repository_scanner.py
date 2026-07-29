import os
from typing import List, Dict

class RepositoryScanner:
    """Scans the repository to understand project structure."""
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.ignore_dirs = {'.git', '__pycache__', 'node_modules', 'logs', '.pytest_cache'}
        
    def scan(self) -> Dict[str, List[str]]:
        """Returns a mapped directory structure of relevant files."""
        structure = {}
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            rel_path = os.path.relpath(root, self.root_dir)
            
            relevant_files = [f for f in files if f.endswith(('.py', '.md', '.json', '.js', '.ts', '.tsx', '.jsx'))]
            if relevant_files:
                structure[rel_path] = relevant_files
        return structure
        
    def find_file(self, filename: str) -> str:
        """Finds the absolute path of a specific file in the repository."""
        for root, dirs, files in os.walk(self.root_dir):
            if filename in files:
                return os.path.join(root, filename)
        return ""
