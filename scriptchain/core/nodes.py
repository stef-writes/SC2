from typing import Dict, Any, List
from .prompts import EnhancedPromptTemplate

class BaseNode:
    def __init__(
        self,
        node_id: str,
        prompt_template: EnhancedPromptTemplate,
        input_keys: List[str],
        output_key: str,
        compress_output: bool = True
    ):
        self.id = node_id
        self.prompt_template = prompt_template
        self.input_keys = input_keys
        self.output_key = output_key
        self.compress_output = compress_output
        
    async def execute(
        self,
        context: Dict[str, Any],
        enable_few_shot: bool
    ) -> Any:
        # Prepare inputs
        inputs = {k: context.get(k) for k in self.input_keys}
        
        # Format prompt with few-shot examples
        if enable_few_shot:
            prompt = self.prompt_template.format(**inputs)
        else:
            prompt = self.prompt_template.base_template.format(**inputs)
            
        # Execute LLM call (pseudo-code)
        result = await self._call_llm(prompt)
        
        return {
            self.output_key: result,
            "_metadata": {
                "compressed": self.compress_output,
                "dependencies": self.input_keys
            }
        }