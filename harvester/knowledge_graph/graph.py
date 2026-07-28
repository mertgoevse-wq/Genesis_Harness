from typing import Dict, Any, List

class KnowledgeGraph:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, node_type: str, metadata: dict):
        # Allowed node types: Agent, Skill, Tool, Pattern, Workflow
        if node_type not in ["Agent", "Skill", "Tool", "Pattern", "Workflow"]:
            raise ValueError(f"Invalid node type: {node_type}")
        self.nodes[node_id] = {"type": node_type, "metadata": metadata}

    def add_edge(self, source_id: str, target_id: str, relation: str):
        self.edges.append({"source": source_id, "target": target_id, "relation": relation})

    def export_graph(self) -> dict:
        return {"nodes": self.nodes, "edges": self.edges}
