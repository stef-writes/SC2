from .context import OptimizedContextManager
from .prompts import EnhancedPromptTemplate, FewShotExample
from .nodes import BaseNode
from .token_tracker import TokenTracker
from typing import Dict, List, Any
import asyncio

class ChainEngine:
    def __init__(self, mode: str = "linear"):
        self.mode = mode
        self.nodes: List[BaseNode] = []
        self.context = OptimizedContextManager()
        self.token_tracker = TokenTracker()
        
    def add_node(self, node: BaseNode):
        """Add a node to the execution chain"""
        self.nodes.append(node)
        
    async def execute(
        self,
        initial_inputs: Dict[str, Any],
        enable_few_shot: bool = True
    ) -> Dict[str, Any]:
        # Initialize context with input data
        for key, value in initial_inputs.items():
            self.context.add_context(key, value)
        
        for node in self.nodes:
            # Get minimal required context
            required_context = {}
            for key in node.input_keys:
                required_context[key] = self.context.get_context(key)
            
            # Execute with few-shot learning
            result = await node.execute(
                context=required_context,
                enable_few_shot=enable_few_shot
            )
            
            # Store optimized context
            self.context.add_context(
                key=node.output_key,
                data=result[node.output_key],
                dependencies=node.input_keys,
                compress=node.compress_output
            )
            
        # Return all node outputs
        result = {}
        for key in initial_inputs:
            result[key] = self.context.get_context(key)
        for node in self.nodes:
            result[node.output_key] = self.context.get_context(node.output_key)
        return result