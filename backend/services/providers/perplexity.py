import json
import os
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from utils.validation import format_template

async def execute_perplexity_function(config: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a Perplexity-based function with the given inputs"""
    try:
        # Import the Perplexity client
        from perplexity import Perplexity
        
        # Get API key from inputs (provided by calling service)
        api_key = inputs.get("api_key")
        if not api_key:
            # Fall back to config or environment as last resort
            api_key = config.get("api_key") or os.environ.get("PERPLEXITY_API_KEY")
            if not api_key:
                raise ValueError("Perplexity API key not provided in request and not found in environment")
        
        print(f"Using Perplexity API with model: {config.get('model', 'sonar-small-online')}")
        
        perplexity = Perplexity(api_key=api_key)
        
        # Get the prompt template and format it with payload values
        prompt_template = config.get("prompt_template", "")
        formatted_prompt = format_template(prompt_template, inputs)
        
        print(f"Formatted prompt (first 200 chars): {formatted_prompt[:200]}...")
        
        response = perplexity.chat.completions.create(
            model=config.get("model", "sonar-small-online"),
            messages=[
                {"role": "system", "content": config.get("system_prompt", "")},
                {"role": "user", "content": formatted_prompt}
            ]
        )
        
        return {"text": response.choices[0].message.content}
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Perplexity SDK not installed. Run 'uv add perplexity' to install.")
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Perplexity API error: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Perplexity API error: {str(e)}")