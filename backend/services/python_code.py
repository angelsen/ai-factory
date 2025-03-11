import importlib.util
import sys
from typing import Dict, Any, Callable
from fastapi import HTTPException

def execute_python_function(config: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Execute Python code function with the given inputs"""
    try:
        # Option 1: Execute from a file path
        if "file_path" in config:
            file_path = config["file_path"]
            function_name = config["function_name"]
            
            print(f"Executing Python function from file: {file_path}, function: {function_name}")
            
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location("dynamic_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["dynamic_module"] = module
            spec.loader.exec_module(module)
            
            # Get and call the function
            function = getattr(module, function_name)
            return function(**inputs)
            
        # Option 2: Execute from code string (less secure, careful with this!)
        elif "code" in config:
            code = config["code"]
            function_name = config["function_name"]
            
            print(f"Executing Python function from code string, function: {function_name}")
            
            # Create a local namespace
            local_namespace = {}
            
            # Execute the code in the namespace
            exec(code, {}, local_namespace)
            
            # Get and call the function from the namespace
            function = local_namespace[function_name]
            return function(**inputs)
        else:
            raise ValueError("Python function config must contain either 'file_path' or 'code'")
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Python execution error: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Python execution error: {str(e)}")