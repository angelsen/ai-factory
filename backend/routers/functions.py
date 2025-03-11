from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
import json

from database import get_db
from models import FunctionConfig
from services.providers.anthropic import execute_anthropic_function
from services.providers.perplexity import execute_perplexity_function
from services.providers.ollama import execute_ollama_function
from services.database_query import execute_database_function
from services.python_code import execute_python_function

router = APIRouter(
    prefix="/api/functions",
    tags=["functions"],
    responses={404: {"description": "Function not found"}},
)

# Request model for function execution
class FunctionExecuteRequest(BaseModel):
    inputs: Dict[str, Any]

@router.post("/{function_name}")
async def execute_function_by_name(
    function_name: str, 
    request_data: FunctionExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute a function by its name with the given inputs"""
    # Enhanced logging
    print(f"Function call request received: {function_name}")
    print(f"Request inputs: {request_data.inputs}")
    
    # Find the function configuration
    function = db.query(FunctionConfig).filter(
        FunctionConfig.name == function_name,
        FunctionConfig.is_active.is_(True)
    ).first()
    
    if not function:
        error_msg = f"Function '{function_name}' not found or inactive"
        print(f"ERROR: {error_msg}")
        raise HTTPException(status_code=404, detail=error_msg)
    
    print(f"Found function configuration: {function.name}, type: {function.implementation_type}")
    
    # Execute the function
    try:
        result = await execute_function_impl(function, request_data.inputs)
        print(f"Function executed successfully")
        return {"success": True, "result": result}
    except Exception as e:
        import traceback
        error_msg = f"Function execution error: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

async def execute_function_impl(function: FunctionConfig, inputs: Dict[str, Any]):
    """Execute a function based on its configuration"""
    try:
        config = json.loads(function.implementation_config)
        print(f"Parsed implementation config for {function.name}")
        
        if function.implementation_type == "anthropic":
            print(f"Executing Anthropic/Claude function implementation")
            return await execute_anthropic_function(config, inputs)
        elif function.implementation_type == "perplexity":
            print(f"Executing Perplexity function implementation")
            return await execute_perplexity_function(config, inputs)
        elif function.implementation_type == "ollama":
            print(f"Executing Ollama function implementation")
            return await execute_ollama_function(config, inputs)
        elif function.implementation_type == "database_query":
            print(f"Executing database query implementation")
            return execute_database_function(config, inputs)
        elif function.implementation_type == "python_code":
            print(f"Executing Python code implementation")
            return execute_python_function(config, inputs)
        else:
            error_msg = f"Unknown implementation type: {function.implementation_type}"
            print(f"ERROR: {error_msg}")
            raise ValueError(error_msg)
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in function implementation config: {str(e)}"
        print(f"ERROR: {error_msg}")
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Error executing function implementation: {str(e)}"
        print(f"ERROR: {error_msg}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise