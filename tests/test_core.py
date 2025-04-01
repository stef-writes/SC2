import pytest
import asyncio
import os
from dotenv import load_dotenv
from core.engine import ChainEngine
from core.nodes import BaseNode
from core.prompts import EnhancedPromptTemplate, FewShotExample
from core.context import OptimizedContextManager

# Load environment variables for testing
load_dotenv()

class MockLLMNode(BaseNode):
    async def _call_llm(self, prompt: str) -> str:
        # Mock LLM response for testing
        return f"Processed: {prompt}"

@pytest.fixture
def engine():
    return ChainEngine(mode="linear")

@pytest.fixture
def mock_prompt_template():
    return EnhancedPromptTemplate(
        template="Process this: {input_text}",
        input_variables=["input_text"],
        examples=[
            FewShotExample(
                input="Hello",
                output="Processed: Hello",
                reasoning="Basic processing"
            )
        ]
    )

@pytest.fixture
def mock_node(mock_prompt_template):
    return MockLLMNode(
        node_id="test_node",
        prompt_template=mock_prompt_template,
        input_keys=["input_text"],
        output_key="result",
        compress_output=True
    )

@pytest.mark.asyncio
async def test_basic_execution(engine, mock_node):
    # Add node to engine
    engine.add_node(mock_node)
    
    # Test input
    initial_inputs = {
        "input_text": "Test input"
    }
    
    # Execute
    result = await engine.execute(initial_inputs)
    
    # Verify result
    assert "test_node" in result
    assert "result" in result["test_node"]
    assert result["test_node"]["result"] == "Processed: Process this: Test input"

@pytest.mark.asyncio
async def test_context_management(engine, mock_node):
    # Add node to engine
    engine.add_node(mock_node)
    
    # Test input
    initial_inputs = {
        "input_text": "Test input"
    }
    
    # Execute
    result = await engine.execute(initial_inputs)
    
    # Verify context
    assert engine.context.get_context("test_node") is not None
    assert engine.context.get_context("input_text") == "Test input"

@pytest.mark.asyncio
async def test_api_key_loaded():
    # Verify API key is loaded
    assert os.getenv("OPENAI_API_KEY") is not None 