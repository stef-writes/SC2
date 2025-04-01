import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from core.engine import ChainEngine
from core.nodes import BaseNode
from core.prompts import EnhancedPromptTemplate, FewShotExample

# Load environment variables
load_dotenv()

class SimpleLLMNode(BaseNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

async def main():
    # Create engine
    engine = ChainEngine(mode="linear")
    
    # Create prompt template
    prompt_template = EnhancedPromptTemplate(
        template="Analyze this text: {text}",
        input_variables=["text"],
        examples=[
            FewShotExample(
                input="The sky is blue",
                output="The sky is blue - This is a simple observation about the color of the sky.",
                reasoning="Basic analysis of a simple statement"
            )
        ]
    )
    
    # Create node
    node = SimpleLLMNode(
        node_id="analyzer",
        prompt_template=prompt_template,
        input_keys=["text"],
        output_key="analysis",
        compress_output=True
    )
    
    # Add node to engine
    engine.add_node(node)
    
    # Test input
    initial_inputs = {
        "text": "The weather is nice today"
    }
    
    # Execute
    result = await engine.execute(initial_inputs)
    
    print("Input:", initial_inputs)
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main()) 