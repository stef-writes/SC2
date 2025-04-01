"""
Lightweight context serialization utilities
"""

import json
from typing import Any, Dict
from ..core.context import ChainContext

def serialize_context(context: ChainContext) -> str:
    """Serialize a chain context to JSON"""
    data = {
        'state': context._state,
        'results': context._results
    }
    return json.dumps(data)

def deserialize_context(json_str: str) -> Dict[str, Any]:
    """Deserialize a JSON string back into a context dictionary"""
    return json.loads(json_str)

def save_context(context: ChainContext, filepath: str) -> None:
    """Save a context to a file"""
    with open(filepath, 'w') as f:
        f.write(serialize_context(context))

def load_context(filepath: str) -> Dict[str, Any]:
    """Load a context from a file"""
    with open(filepath, 'r') as f:
        return deserialize_context(f.read()) 