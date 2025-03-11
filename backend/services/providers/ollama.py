import json
import os
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from utils.validation import format_template

async def execute_ollama_function(config: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Execute an Ollama-based function with the given inputs"""
    try:
        # Import the Ollama client
        import ollama
        
        print(f"Using Ollama with model: {config.get('model', 'llama3')}")
        
        # Get the host from config or environment
        host = config.get("host") or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        
        # Configure Ollama client
        ollama.client.base_url = host
        
        # Get the prompt template and format it with payload values
        prompt_template = config.get("prompt_template", "")
        formatted_prompt = format_template(prompt_template, inputs)
        
        system_prompt = config.get("system_prompt", "")
        
        print(f"Formatted prompt (first 200 chars): {formatted_prompt[:200]}...")
        
        # Create the message payload
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": formatted_prompt})
        
        # Make Ollama API call
        response = ollama.chat(
            model=config.get("model", "llama3"),
            messages=messages,
            options={
                "temperature": config.get("temperature", 0.7),
                "top_p": config.get("top_p", 0.9),
                "num_predict": config.get("max_tokens", 1024)
            }
        )
        
        return {"text": response["message"]["content"]}
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Ollama Python SDK not installed. Run 'uv add ollama' to install.")
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Ollama API error: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")