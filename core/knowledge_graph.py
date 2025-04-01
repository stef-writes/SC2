from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import networkx as nx
from datetime import datetime

@dataclass
class Node:
    id: str
    type: str
    content: Any
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

@dataclass
class Edge:
    source: str
    target: str
    type: str
    metadata: Dict[str, Any]
    created_at: datetime

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, Node] = {}
        self.edge_types = set()
        
    def add_node(self, node_id: str, node_type: str, content: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a node to the knowledge graph."""
        now = datetime.now()
        node = Node(
            id=node_id,
            type=node_type,
            content=content,
            metadata=metadata or {},
            created_at=now,
            updated_at=now
        )
        self.nodes[node_id] = node
        self.graph.add_node(node_id, **{
            'type': node_type,
            'content': content,
            'metadata': metadata or {},
            'created_at': now,
            'updated_at': now
        })
        
    def add_edge(self, source_id: str, target_id: str, edge_type: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add an edge between two nodes."""
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Source or target node does not exist")
            
        now = datetime.now()
        edge = Edge(
            source=source_id,
            target=target_id,
            type=edge_type,
            metadata=metadata or {},
            created_at=now
        )
        self.edge_types.add(edge_type)
        self.graph.add_edge(source_id, target_id, **{
            'type': edge_type,
            'metadata': metadata or {},
            'created_at': now
        })
        
    def get_node(self, node_id: str) -> Optional[Node]:
        """Retrieve a node by its ID."""
        return self.nodes.get(node_id)
        
    def get_connected_nodes(self, node_id: str, direction: str = 'both') -> List[Node]:
        """Get nodes connected to a given node."""
        if direction == 'in':
            connected_ids = list(self.graph.predecessors(node_id))
        elif direction == 'out':
            connected_ids = list(self.graph.successors(node_id))
        else:  # both
            connected_ids = list(self.graph.neighbors(node_id))
        return [self.nodes[node_id] for node_id in connected_ids]
        
    def query(self, query_type: str, **kwargs) -> List[Node]:
        """Query nodes based on type and metadata."""
        results = []
        for node_id, node in self.nodes.items():
            if node.type == query_type:
                if all(node.metadata.get(k) == v for k, v in kwargs.items()):
                    results.append(node)
        return results
        
    def get_path(self, source_id: str, target_id: str) -> Optional[List[Node]]:
        """Find the shortest path between two nodes."""
        try:
            path = nx.shortest_path(self.graph, source_id, target_id)
            return [self.nodes[node_id] for node_id in path]
        except nx.NetworkXNoPath:
            return None
            
    def get_subgraph(self, node_ids: List[str]) -> 'KnowledgeGraph':
        """Create a subgraph containing only the specified nodes."""
        subgraph = KnowledgeGraph()
        for node_id in node_ids:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                subgraph.add_node(
                    node_id=node.id,
                    node_type=node.type,
                    content=node.content,
                    metadata=node.metadata
                )
                
        # Add edges between nodes in the subgraph
        for source_id in node_ids:
            for target_id in node_ids:
                if self.graph.has_edge(source_id, target_id):
                    edge_data = self.graph.get_edge_data(source_id, target_id)
                    subgraph.add_edge(
                        source_id=source_id,
                        target_id=target_id,
                        edge_type=edge_data['type'],
                        metadata=edge_data['metadata']
                    )
                    
        return subgraph
        
    def merge(self, other: 'KnowledgeGraph') -> None:
        """Merge another knowledge graph into this one."""
        for node_id, node in other.nodes.items():
            if node_id not in self.nodes:
                self.add_node(
                    node_id=node.id,
                    node_type=node.type,
                    content=node.content,
                    metadata=node.metadata
                )
                
        for edge in other.graph.edges(data=True):
            source_id, target_id = edge[0], edge[1]
            if not self.graph.has_edge(source_id, target_id):
                self.add_edge(
                    source_id=source_id,
                    target_id=target_id,
                    edge_type=edge[2]['type'],
                    metadata=edge[2]['metadata']
                ) 