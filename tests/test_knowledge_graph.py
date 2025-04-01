import pytest
from datetime import datetime
from core.knowledge_graph import KnowledgeGraph, Node, Edge

@pytest.fixture
def knowledge_graph():
    return KnowledgeGraph()

def test_add_node(knowledge_graph):
    # Test adding a node
    knowledge_graph.add_node(
        node_id="test_node",
        node_type="text",
        content="Test content",
        metadata={"source": "test"}
    )
    
    # Verify node was added correctly
    node = knowledge_graph.get_node("test_node")
    assert node is not None
    assert node.id == "test_node"
    assert node.type == "text"
    assert node.content == "Test content"
    assert node.metadata == {"source": "test"}

def test_add_edge(knowledge_graph):
    # Add two nodes
    knowledge_graph.add_node("node1", "text", "Content 1")
    knowledge_graph.add_node("node2", "text", "Content 2")
    
    # Add edge between nodes
    knowledge_graph.add_edge(
        source_id="node1",
        target_id="node2",
        edge_type="relates_to",
        metadata={"weight": 1}
    )
    
    # Verify edge was added
    connected_nodes = knowledge_graph.get_connected_nodes("node1", direction="out")
    assert len(connected_nodes) == 1
    assert connected_nodes[0].id == "node2"

def test_query(knowledge_graph):
    # Add nodes with different types
    knowledge_graph.add_node("node1", "text", "Content 1", {"tag": "important"})
    knowledge_graph.add_node("node2", "text", "Content 2", {"tag": "normal"})
    knowledge_graph.add_node("node3", "image", "Image 1", {"tag": "important"})
    
    # Query nodes by type and metadata
    results = knowledge_graph.query("text", tag="important")
    assert len(results) == 1
    assert results[0].id == "node1"

def test_get_path(knowledge_graph):
    # Create a chain of nodes
    knowledge_graph.add_node("node1", "text", "Content 1")
    knowledge_graph.add_node("node2", "text", "Content 2")
    knowledge_graph.add_node("node3", "text", "Content 3")
    
    # Add edges
    knowledge_graph.add_edge("node1", "node2", "next")
    knowledge_graph.add_edge("node2", "node3", "next")
    
    # Find path
    path = knowledge_graph.get_path("node1", "node3")
    assert len(path) == 3
    assert path[0].id == "node1"
    assert path[1].id == "node2"
    assert path[2].id == "node3"

def test_get_subgraph(knowledge_graph):
    # Create a graph with multiple nodes
    knowledge_graph.add_node("node1", "text", "Content 1")
    knowledge_graph.add_node("node2", "text", "Content 2")
    knowledge_graph.add_node("node3", "text", "Content 3")
    
    # Add edges
    knowledge_graph.add_edge("node1", "node2", "relates_to")
    knowledge_graph.add_edge("node2", "node3", "relates_to")
    
    # Get subgraph
    subgraph = knowledge_graph.get_subgraph(["node1", "node2"])
    assert len(subgraph.nodes) == 2
    assert "node1" in subgraph.nodes
    assert "node2" in subgraph.nodes
    assert len(subgraph.graph.edges) == 1

def test_merge(knowledge_graph):
    # Create two graphs
    graph1 = KnowledgeGraph()
    graph1.add_node("node1", "text", "Content 1")
    graph1.add_node("node2", "text", "Content 2")
    graph1.add_edge("node1", "node2", "relates_to")
    
    graph2 = KnowledgeGraph()
    graph2.add_node("node2", "text", "Content 2")
    graph2.add_node("node3", "text", "Content 3")
    graph2.add_edge("node2", "node3", "relates_to")
    
    # Merge graphs
    graph1.merge(graph2)
    
    # Verify merged graph
    assert len(graph1.nodes) == 3
    assert len(graph1.graph.edges) == 2
    assert "node3" in graph1.nodes 