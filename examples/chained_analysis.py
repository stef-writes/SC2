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

class ContentAnalyzerNode(BaseLLMNode):
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Analyze the content and extract key information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

class InsightGeneratorNode(BaseLLMNode):
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate insights based on the analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

class RecommendationNode(BaseLLMNode):
    async def _call_llm(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate recommendations based on the insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

async def main():
    # Create engine
    engine = ChainEngine(mode="linear")
    
    # Create prompt templates
    analysis_template = EnhancedPromptTemplate(
        template="Analyze this content: {content}",
        input_variables=["content"],
        examples=[
            FewShotExample(
                input="The company's revenue increased by 25% in Q1.",
                output="Key metrics: Revenue growth of 25% in Q1",
                reasoning="Extracting key performance indicators"
            )
        ]
    )
    
    insight_template = EnhancedPromptTemplate(
        template="Generate insights from this analysis: {analysis}",
        input_variables=["analysis"],
        examples=[
            FewShotExample(
                input="Key metrics: Revenue growth of 25% in Q1",
                output="Strong growth indicates successful business strategy",
                reasoning="Interpreting the analysis"
            )
        ]
    )
    
    recommendation_template = EnhancedPromptTemplate(
        template="Generate recommendations based on these insights: {insights}",
        input_variables=["insights"],
        examples=[
            FewShotExample(
                input="Strong growth indicates successful business strategy",
                output="Continue current strategy and consider expansion",
                reasoning="Deriving actionable recommendations"
            )
        ]
    )
    
    # Create nodes with dependencies
    analyzer = ContentAnalyzerNode(
        node_id="content_analyzer",
        prompt_template=analysis_template,
        input_keys=["content"],
        output_key="analysis",
        compress_output=True
    )
    
    insight_generator = InsightGeneratorNode(
        node_id="insight_generator",
        prompt_template=insight_template,
        input_keys=["analysis"],  # Depends on analyzer's output
        output_key="insights",
        compress_output=True
    )
    
    recommender = RecommendationNode(
        node_id="recommender",
        prompt_template=recommendation_template,
        input_keys=["insights"],  # Depends on insight_generator's output
        output_key="recommendations",
        compress_output=True
    )
    
    # Add nodes to engine in order of dependencies
    engine.add_node(analyzer)
    engine.add_node(insight_generator)
    engine.add_node(recommender)
    
    # Test input
    initial_inputs = {
        "content": "The company's Q1 performance shows significant improvement. Revenue increased by 25%, customer satisfaction rose by 15%, and employee retention improved by 10%. Market share expanded in key segments, and new product launches were well-received."
    }
    
    # Execute
    result = await engine.execute(initial_inputs)
    
    print("\nInput Content:")
    print(initial_inputs["content"])
    print("\nAnalysis:")
    print(result["content_analyzer"]["analysis"])
    print("\nInsights:")
    print(result["insight_generator"]["insights"])
    print("\nRecommendations:")
    print(result["recommender"]["recommendations"])
    
    # Print token usage
    print("\nToken Usage:")
    print(engine.token_tracker.get_usage())

if __name__ == "__main__":
    asyncio.run(main()) 