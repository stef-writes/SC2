from scriptchain.core import BaseNode
from langchain.prompts import PromptTemplate
import openai

class TextAnalyzerNode(BaseNode):
    """A node that analyzes text using OpenAI's GPT model."""
    
    def __init__(self):
        super().__init__(
            name="text_analyzer",
            description="Analyzes input text for sentiment, topics, and key points",
            required_context=["text"]
        )
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""Analyze the following text and provide:
1. Overall sentiment (positive, negative, or neutral)
2. Main topics
3. Key points

Text: {text}

Please provide your analysis in JSON format with the following structure:
{
    "sentiment": "string",
    "topics": ["string"],
    "key_points": ["string"]
}"""
        )
    
    async def _call_llm(self, prompt: str) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content 