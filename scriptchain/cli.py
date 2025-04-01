import click
import asyncio
import json
from pathlib import Path
from typing import Dict, Any
import importlib.util
import sys
import traceback

from .core import ChainEngine, BaseNode
from .core.prompts import EnhancedPromptTemplate

def load_custom_node(node_path: str) -> BaseNode:
    """Load a custom node from a Python file."""
    path = Path(node_path)
    if not path.exists():
        raise click.ClickException(f"Node file not found: {node_path}")
    
    spec = importlib.util.spec_from_file_location("custom_node", path)
    if not spec or not spec.loader:
        raise click.ClickException(f"Could not load node from: {node_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Find the first BaseNode subclass
    for name, obj in module.__dict__.items():
        if (isinstance(obj, type) and 
            issubclass(obj, BaseNode) and 
            obj != BaseNode):
            return obj()
    
    raise click.ClickException(f"No valid node class found in {node_path}")

@click.group()
def cli():
    """ScriptChain CLI - A lightweight, efficient chain execution framework for LLM-powered workflows."""
    pass

@cli.command()
@click.argument('node_path', type=click.Path(exists=True))
@click.option('--input', '-i', help='Input data as JSON string')
@click.option('--input-file', '-f', type=click.Path(exists=True), help='Input data from JSON file')
@click.option('--output-file', '-o', type=click.Path(), help='Output file for results')
def run(node_path: str, input: str, input_file: str, output_file: str):
    """Run a custom node with the given input."""
    try:
        # Load the custom node
        node = load_custom_node(node_path)
        
        # Get input data
        if input:
            input_data = json.loads(input)
        elif input_file:
            with open(input_file) as f:
                input_data = json.load(f)
        else:
            raise click.ClickException("Either --input or --input-file must be provided")
        
        # Create and run the engine
        engine = ChainEngine()
        engine.add_node(node)
        
        async def execute():
            result = await engine.execute(input_data)
            return result
        
        result = asyncio.run(execute())
        
        # Output results
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Results written to {output_file}")
        else:
            click.echo(json.dumps(result, indent=2))
            
    except Exception as e:
        click.echo(f"Error details: {str(e)}", err=True)
        click.echo("Traceback:", err=True)
        click.echo(traceback.format_exc(), err=True)
        raise click.ClickException(str(e))

@cli.command()
@click.argument('node_path', type=click.Path(exists=True))
def info(node_path: str):
    """Display information about a custom node."""
    try:
        node = load_custom_node(node_path)
        click.echo(f"Node ID: {node.id}")
        click.echo(f"Input Keys: {', '.join(node.input_keys)}")
        click.echo(f"Output Key: {node.output_key}")
        click.echo(f"Compress Output: {node.compress_output}")
        if hasattr(node, 'prompt_template'):
            click.echo(f"Prompt Template:\n{node.prompt_template.base_template.template}")
            if node.prompt_template.examples:
                click.echo("\nExamples:")
                for i, ex in enumerate(node.prompt_template.examples, 1):
                    click.echo(f"\nExample {i}:")
                    click.echo(f"Input: {ex.input}")
                    click.echo(f"Output: {ex.output}")
                    if ex.reasoning:
                        click.echo(f"Reasoning: {ex.reasoning}")
    except Exception as e:
        click.echo(f"Error details: {str(e)}", err=True)
        click.echo("Traceback:", err=True)
        click.echo(traceback.format_exc(), err=True)
        raise click.ClickException(str(e))

@cli.command()
@click.argument('node_path', type=click.Path(exists=True))
def test(node_path: str):
    """Run tests for a custom node."""
    try:
        node = load_custom_node(node_path)
        engine = ChainEngine()
        engine.add_node(node)
        
        # Create a test input
        test_input = {key: f"test_{key}" for key in node.input_keys}
        
        async def execute():
            result = await engine.execute(test_input)
            return result
        
        result = asyncio.run(execute())
        click.echo("Test successful!")
        click.echo("Result:")
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        raise click.ClickException(str(e))

def main():
    cli()

if __name__ == '__main__':
    main() 