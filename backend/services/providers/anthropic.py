import json
import os
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from utils.validation import format_template

async def execute_anthropic_function(config: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a Claude-based function with the given inputs"""
    try:
        # Import the Anthropic client only when needed
        from anthropic import Anthropic
        
        # Get API key from inputs (provided by calling service)
        api_key = inputs.get("api_key")
        if not api_key:
            # Fall back to config or environment as last resort
            api_key = config.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key not provided in request and not found in environment")
        
        print(f"Using Claude API with model: {config.get('model', 'claude-3-5-sonnet-20240620')}")
        
        anthropic = Anthropic(api_key=api_key)
        
        # Get the prompt template and format it with payload values
        prompt_template = config.get("prompt_template", "")
        formatted_prompt = format_template(prompt_template, inputs)
        
        print(f"Formatted prompt (first 200 chars): {formatted_prompt[:200]}...")
        
        # Determine if we should use tools/function calling
        tools = config.get("tools")
        
        # Make Claude API call
        if tools:
            print(f"Making Claude API call with tools")
            response = anthropic.messages.create(
                model=config.get("model", "claude-3-5-sonnet-20240620"),
                max_tokens=config.get("max_tokens", 1000),
                system=config.get("system_prompt", ""),
                messages=[{"role": "user", "content": formatted_prompt}],
                tools=tools
            )
            
            print(f"Claude API response received, content types: {[c.type for c in response.content]}")
            
            # Extract tool calls from the response
            for i, content in enumerate(response.content):
                print(f"Examining content item {i}, type: {content.type}")
                
                if content.type == "tool_use":
                    print(f"Found tool_use content")
                    
                    if hasattr(content, 'name') and content.name:
                        print(f"Found tool with name: {content.name}")
                        
                        if isinstance(content.input, dict):
                            print(f"Input is already a dictionary")
                            return content.input
                        else:
                            print(f"Parsing input as JSON: {content.input}")
                            return json.loads(content.input)
            
            # Fallback to text response if no tool call
            print(f"No tool call found, falling back to text response")
            if response.content and hasattr(response.content[0], 'text'):
                return {"text": response.content[0].text}
            return {"text": "No text content in response"}
        else:
            # Simple completion without tools
            print(f"Making simple Claude API call without tools")
            response = anthropic.messages.create(
                model=config.get("model", "claude-3-5-sonnet-20240620"),
                max_tokens=config.get("max_tokens", 1000),
                system=config.get("system_prompt", ""),
                messages=[{"role": "user", "content": formatted_prompt}]
            )
            return {"text": response.content[0].text}
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Claude API error: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")