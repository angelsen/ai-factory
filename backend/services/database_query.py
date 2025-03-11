from typing import Dict, Any
from fastapi import HTTPException
from sqlalchemy import create_engine, text
from utils.validation import format_template

def execute_database_function(config: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a database query function with the given inputs"""
    try:
        # Get the connection string from config
        connection_string = config.get("connection_string", "sqlite:///./ai_factory.db")
        
        # Get the query template and format it with inputs
        query_template = config.get("query_template", "")
        formatted_query = format_template(query_template, inputs)
        
        print(f"Executing database query: {formatted_query[:200]}...")
        
        # Execute the query (with care for SQL injection protection)
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            result = connection.execute(text(formatted_query))
            if result.returns_rows:
                rows = [dict(row) for row in result]
                return {"results": rows}
            return {"success": True, "affected_rows": result.rowcount}
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Database query error: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")