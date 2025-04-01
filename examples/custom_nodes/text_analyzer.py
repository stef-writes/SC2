from scriptchain.core import BaseNode
from scriptchain.core.prompts import EnhancedPromptTemplate, FewShotExample
from openai import AsyncOpenAI
import os
import json

class TextAnalyzerNode(BaseNode):
    """A node that analyzes text using OpenAI's GPT model."""
    
    def __init__(self):
        template = EnhancedPromptTemplate(
            template="""Analyze the following text and provide:
1. Overall sentiment (positive, negative, or neutral)
2. Main topics
3. Key points

Text: {text}

Please provide your analysis in JSON format with the following structure:
{{
    "sentiment": "string",
    "topics": ["string"],
    "key_points": ["string"]
}}""",
            input_variables=["text"],
            examples=[
                FewShotExample(
                    input="The weather is nice today and I'm feeling great!",
                    output="""{"sentiment": "positive", "topics": ["weather", "personal mood"], "key_points": ["Good weather", "Positive emotional state"]}""",
                    reasoning="The text expresses positive sentiment about both the weather and personal feelings."
                )
            ]
        )
        
        super().__init__(
            node_id="text_analyzer",
            prompt_template=template,
            input_keys=["text"],
            output_key="analysis",
            compress_output=True
        )
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response.choices[0].message.content
        try:
            # Parse the JSON response
            return json.loads(result)
        except json.JSONDecodeError:
            # If parsing fails, return the raw string
            return result 