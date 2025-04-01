# ScriptChain

A lightweight, efficient chain execution framework for LLM-powered workflows. ScriptChain enables developers to create, manage, and execute complex AI workflows with minimal boilerplate code.

## 🌟 Key Features

### Core Capabilities
- **Modular Node System**: Create reusable, self-contained nodes for different AI tasks
- **Context Management**: Efficient handling of data flow between nodes
- **Few-Shot Learning Support**: Built-in support for example-based prompting
- **Token Tracking**: Monitor and optimize LLM token usage
- **Async Execution**: Native async/await support for improved performance
- **OpenAI Integration**: Seamless integration with OpenAI's API
- **Extensible Design**: Easy to add new node types and capabilities

### Technical Advantages
- **Type Safety**: Full type hints and validation using Pydantic
- **Efficient Serialization**: Fast context serialization with msgpack
- **Memory Optimization**: Smart context compression and management
- **Dependency Management**: Clear node dependencies and execution order
- **Error Handling**: Robust error handling and recovery
- **Testing Support**: Comprehensive testing utilities and fixtures

## 🚀 Quick Start

### Installation
```bash
pip install scriptchain
```

### Basic Usage
```python
from scriptchain import ChainEngine, BaseNode
from langchain.prompts import PromptTemplate
import openai

# Create a prompt template
template = PromptTemplate(
    input_variables=["text"],
    template="Analyze the following text: {text}"
)

# Create a custom node
class TextAnalyzerNode(BaseNode):
    def __init__(self):
        super().__init__(
            name="text_analyzer",
            description="Analyzes input text",
            required_context=["text"]
        )
        self.prompt = template

    async def _call_llm(self, prompt: str) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

# Create and run the chain
async def main():
    engine = ChainEngine()
    engine.add_node(TextAnalyzerNode())
    
    result = await engine.execute({
        "text": "The weather is nice today"
    })
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 🏗️ Architecture

### Core Components

#### ChainEngine
The main orchestrator that:
- Manages node execution order
- Handles context flow
- Tracks token usage
- Provides execution statistics

#### BaseNode
The foundation for all nodes that:
- Defines the node interface
- Handles context validation
- Manages prompt templates
- Provides async execution

#### Context Management
Efficient context handling that:
- Validates required context
- Manages context dependencies
- Optimizes memory usage
- Supports context compression

### Data Flow
1. Input data is validated and normalized
2. Context is gathered for each node
3. Nodes execute in dependency order
4. Results are collected and returned

## 💡 Use Cases

### Content Analysis
- Text classification
- Sentiment analysis
- Topic extraction
- Content summarization

### Data Processing
- Data cleaning
- Format conversion
- Validation
- Enrichment

### Decision Making
- Classification
- Recommendation
- Risk assessment
- Priority scoring

### Knowledge Extraction
- Entity recognition
- Relationship extraction
- Fact verification
- Knowledge graph building

## 🎯 Value Proposition

### For Developers
- **Reduced Boilerplate**: Focus on business logic, not infrastructure
- **Type Safety**: Catch errors early with comprehensive type checking
- **Async Support**: Better performance with native async/await
- **Easy Testing**: Built-in testing support and fixtures
- **Flexible Architecture**: Adapt to changing requirements easily

### For Organizations
- **Cost Efficiency**: Optimize token usage and API calls
- **Maintainability**: Clear, modular code structure
- **Scalability**: Easy to add new capabilities
- **Reliability**: Robust error handling and recovery
- **Performance**: Efficient context management and async execution

## 🔧 Advanced Usage

### Custom Node Types
```python
class CustomNode(BaseNode):
    def __init__(self):
        super().__init__(
            name="custom_node",
            description="Custom node description",
            required_context=["input1", "input2"]
        )
        self.prompt = PromptTemplate(
            input_variables=["input1", "input2"],
            template="Process {input1} and {input2}"
        )

    async def _call_llm(self, prompt: str) -> str:
        # Custom LLM call implementation
        pass
```

### Chain Configuration
```python
engine = ChainEngine()
engine.add_node(Node1())
engine.add_node(Node2())
engine.add_node(Node3())

# Execute with custom context
result = await engine.execute({
    "input1": "value1",
    "input2": "value2"
})
```

## 📊 Performance Considerations

### Token Optimization
- Smart context compression
- Efficient prompt management
- Token usage tracking
- Cost optimization strategies

### Memory Management
- Context cleanup
- Resource optimization
- Memory-efficient serialization
- Garbage collection

### Async Benefits
- Non-blocking operations
- Improved throughput
- Better resource utilization
- Scalable execution

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for their powerful API
- LangChain for inspiration
- The Python community for excellent tools and libraries

## 💬 Support

For support, please open an issue in the GitHub repository. 