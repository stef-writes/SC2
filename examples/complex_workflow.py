import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from core.engine import ChainEngine
from core.nodes import BaseNode
from core.prompts import EnhancedPromptTemplate, FewShotExample

# Load environment variables
load_dotenv()

class BaseLLMNode(BaseNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

class TopicExtractorNode(BaseLLMNode):
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract the main topics from the text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

class SentimentAnalyzerNode(BaseLLMNode):
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Analyze the sentiment of the text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

class SummaryGeneratorNode(BaseLLMNode):
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate a concise summary of the text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

async def main():
    # Create engine
    engine = ChainEngine(mode="linear")
    
    # Create prompt templates
    topic_template = EnhancedPromptTemplate(
        template="Extract main topics from: {text}",
        input_variables=["text"],
        examples=[
            FewShotExample(
                input="The weather is nice today and the birds are singing.",
                output="Topics: weather, birds, nature",
                reasoning="Extracting key subjects from the text"
            )
        ]
    )
    
    sentiment_template = EnhancedPromptTemplate(
        template="Analyze sentiment of: {text}",
        input_variables=["text"],
        examples=[
            FewShotExample(
                input="I love this beautiful day!",
                output="Positive sentiment",
                reasoning="Identifying positive emotional tone"
            )
        ]
    )
    
    summary_template = EnhancedPromptTemplate(
        template="Summarize: {text}",
        input_variables=["text"],
        examples=[
            FewShotExample(
                input="The quick brown fox jumps over the lazy dog.",
                output="A fox jumps over a dog.",
                reasoning="Creating a concise summary"
            )
        ]
    )
    
    # Create nodes
    topic_node = TopicExtractorNode(
        node_id="topic_extractor",
        prompt_template=topic_template,
        input_keys=["text"],
        output_key="topics",
        compress_output=True
    )
    
    sentiment_node = SentimentAnalyzerNode(
        node_id="sentiment_analyzer",
        prompt_template=sentiment_template,
        input_keys=["text"],
        output_key="sentiment",
        compress_output=True
    )
    
    summary_node = SummaryGeneratorNode(
        node_id="summary_generator",
        prompt_template=summary_template,
        input_keys=["text"],
        output_key="summary",
        compress_output=True
    )
    
    # Add nodes to engine
    engine.add_node(topic_node)
    engine.add_node(sentiment_node)
    engine.add_node(summary_node)
    
    # Test input
    initial_inputs = {
        "text": "The sun is shining brightly in the clear blue sky. Birds are chirping happily in the trees, and a gentle breeze rustles through the leaves. It's a perfect day for a walk in the park."
    }
    
    # Execute
    result = await engine.execute(initial_inputs)
    
    print("\nInput Text:")
    print(initial_inputs["text"])
    print("\nResults:")
    print(f"Topics: {result['topic_extractor']['topics']}")
    print(f"Sentiment: {result['sentiment_analyzer']['sentiment']}")
    print(f"Summary: {result['summary_generator']['summary']}")
    
    # Print token usage
    print("\nToken Usage:")
    print(engine.token_tracker.get_usage())

if __name__ == "__main__":
    asyncio.run(main()) 