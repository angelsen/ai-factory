import json
from typing import Dict, Any, Optional
from fastapi import HTTPException

def validate_json_schema(schema_str: str) -> Dict[str, Any]:
    """Validate that a string contains valid JSON schema"""
    try:
        schema = json.loads(schema_str)
        # TODO: Add more advanced schema validation if needed
        return schema
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON schema: {str(e)}")

def validate_inputs(inputs: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """Validate inputs against a JSON schema"""
    # TODO: Add more sophisticated schema validation
    # For now, just check required fields
    if "properties" in schema and "required" in schema:
        for field in schema.get("required", []):
            if field not in inputs:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    return inputs

def format_template(template: str, inputs: Dict[str, Any]) -> str:
    """Format a template string with input values"""
    try:
        return template.format(**inputs)
    except KeyError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Missing required input: {str(e)}. Available inputs: {list(inputs.keys())}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting template: {str(e)}")