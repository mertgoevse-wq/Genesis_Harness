import ast

class CodeAnalyzer:
    """Analyzes code syntax and structure."""
    
    def analyze_python_file(self, filepath: str) -> dict:
        """Parses a Python file to extract classes and functions."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            return {
                "file": filepath,
                "classes": classes,
                "functions": functions
            }
        except Exception as e:
            return {"error": str(e)}
