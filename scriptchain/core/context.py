from pydantic import BaseModel
from typing import Dict, Any, List
import msgpack

class ContextItem(BaseModel):
    data: Any
    dependencies: List[str] = []
    compressed: bool = False

class OptimizedContextManager:
    def __init__(self):
        self.context: Dict[str, ContextItem] = {}
        self.dependency_graph: Dict[str, List[str]] = {}

    def add_context(
        self,
        key: str,
        data: Any,
        dependencies: List[str] = [],
        compress: bool = True
    ):
        # Store only dependency chain
        self.dependency_graph[key] = dependencies
        
        # Compress large data payloads
        if compress and isinstance(data, (str, bytes)):
            self.context[key] = ContextItem(
                data=msgpack.packb(data),
                dependencies=dependencies,
                compressed=True
            )
        else:
            self.context[key] = ContextItem(
                data=data,
                dependencies=dependencies,
                compressed=False
            )

    def get_context(self, key: str) -> Any:
        item = self.context.get(key)
        if not item:
            return None
            
        # Decompress if needed
        if item.compressed:
            return msgpack.unpackb(item.data)
        return item.data

    def get_chain(self, keys: List[str]) -> Dict[str, Any]:
        """Get minimal context needed for a set of keys"""
        required = set()
        for key in keys:
            required.update(self.dependency_graph.get(key, []))
            required.add(key)
            
        return {k: self.get_context(k) for k in required}