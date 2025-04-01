import asyncio
import os
from dotenv import load_dotenv
from core.engine import ChainEngine
from core.nodes import BaseLLMNode
from core.knowledge_graph import KnowledgeGraph
from core.prompt_template import EnhancedPromptTemplate

# Load environment variables
load_dotenv()

class TopicExtractorNode(BaseLLMNode):
    def __init__(self, node_id: str):
        super().__init__(
            node_id=node_id,
            input_keys=["text"],
            output_key="topics",
            prompt_template=EnhancedPromptTemplate(
                system_prompt="You are a topic extraction expert. Extract the main topics from the given text.",
                human_template="Extract the main topics from this text:\n{text}",
                few_shot_examples=[
                    {
                        "input": {"text": "The weather is nice today and the sun is shining."},
                        "output": "Topics: weather, sun, day"
                    }
                ]
            )
        )

class EntityExtractorNode(BaseLLMNode):
    def __init__(self, node_id: str):
        super().__init__(
            node_id=node_id,
            input_keys=["text"],
            output_key="entities",
            prompt_template=EnhancedPromptTemplate(
                system_prompt="You are an entity extraction expert. Extract named entities from the given text.",
                human_template="Extract named entities from this text:\n{text}",
                few_shot_examples=[
                    {
                        "input": {"text": "John went to New York on Monday."},
                        "output": "Entities: John (person), New York (location), Monday (date)"
                    }
                ]
            )
        )

class RelationExtractorNode(BaseLLMNode):
    def __init__(self, node_id: str):
        super().__init__(
            node_id=node_id,
            input_keys=["text", "entities"],
            output_key="relations",
            prompt_template=EnhancedPromptTemplate(
                system_prompt="You are a relation extraction expert. Extract relationships between entities in the text.",
                human_template="Extract relationships between these entities in the text:\nText: {text}\nEntities: {entities}",
                few_shot_examples=[
                    {
                        "input": {
                            "text": "John works at Google in Mountain View.",
                            "entities": "John (person), Google (organization), Mountain View (location)"
                        },
                        "output": "Relations: John works_at Google, Google located_in Mountain View"
                    }
                ]
            )
        )

async def main():
    # Initialize the knowledge graph
    kg = KnowledgeGraph()
    
    # Create the chain engine
    engine = ChainEngine()
    
    # Create nodes
    topic_node = TopicExtractorNode("topic_extractor")
    entity_node = EntityExtractorNode("entity_extractor")
    relation_node = RelationExtractorNode("relation_extractor")
    
    # Add nodes to the engine
    engine.add_node(topic_node)
    engine.add_node(entity_node)
    engine.add_node(relation_node)
    
    # Sample text for analysis
    text = "John works at Google in Mountain View. The weather is nice today and the sun is shining."
    
    # Execute the chain
    result = await engine.execute({"text": text})
    
    # Add nodes to knowledge graph
    kg.add_node(
        node_id="text_1",
        node_type="text",
        content=text,
        metadata={"source": "input"}
    )
    
    # Add topic node
    kg.add_node(
        node_id="topics_1",
        node_type="topics",
        content=result["topics"],
        metadata={"source": "topic_extractor"}
    )
    kg.add_edge("text_1", "topics_1", "has_topics")
    
    # Add entity node
    kg.add_node(
        node_id="entities_1",
        node_type="entities",
        content=result["entities"],
        metadata={"source": "entity_extractor"}
    )
    kg.add_edge("text_1", "entities_1", "has_entities")
    
    # Add relation node
    kg.add_node(
        node_id="relations_1",
        node_type="relations",
        content=result["relations"],
        metadata={"source": "relation_extractor"}
    )
    kg.add_edge("entities_1", "relations_1", "has_relations")
    
    # Query the knowledge graph
    print("\nKnowledge Graph Analysis:")
    print("------------------------")
    
    # Get all topics
    topics = kg.query("topics")
    print("\nTopics found:")
    for topic in topics:
        print(f"- {topic.content}")
    
    # Get all entities
    entities = kg.query("entities")
    print("\nEntities found:")
    for entity in entities:
        print(f"- {entity.content}")
    
    # Get all relations
    relations = kg.query("relations")
    print("\nRelations found:")
    for relation in relations:
        print(f"- {relation.content}")
    
    # Get path from text to relations
    path = kg.get_path("text_1", "relations_1")
    print("\nPath from text to relations:")
    for node in path:
        print(f"- {node.type}: {node.content}")

if __name__ == "__main__":
    asyncio.run(main()) 