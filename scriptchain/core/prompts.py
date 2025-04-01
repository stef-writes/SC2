from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List, Dict, Any

class FewShotExample(BaseModel):
    input: str
    output: str
    reasoning: str = ""

class EnhancedPromptTemplate:
    def __init__(
        self,
        template: str,
        input_variables: List[str],
        examples: List[FewShotExample] = None,
        example_header: str = "Examples:"
    ):
        self.base_template = PromptTemplate(
            template=template,
            input_variables=input_variables
        )
        self.examples = examples or []
        self.example_header = example_header
        
    def format(self, **kwargs) -> str:
        # Format the base template first
        base_result = self.base_template.format(**kwargs)
        
        # If there are no examples, just return the base result
        if not self.examples:
            return base_result
            
        # Format examples
        example_str = "\n\n".join(
            [f"Input: {ex.input}\nOutput: {ex.output}\nReasoning: {ex.reasoning}" 
             for ex in self.examples]
        )
        
        # Combine everything
        return f"{self.example_header}\n{example_str}\n\n{base_result}"