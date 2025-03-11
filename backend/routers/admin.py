from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import json

from database import get_db
from models import FunctionConfig
from utils.validation import validate_json_schema

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.get("/functions")
async def list_functions(db: Session = Depends(get_db)):
    """List all function configurations"""
    functions = db.query(FunctionConfig).all()
    return [
        {
            "id": func.id,
            "name": func.name,
            "description": func.description,
            "implementation_type": func.implementation_type,
            "is_active": func.is_active,
            "created_at": func.created_at,
            "updated_at": func.updated_at
        }
        for func in functions
    ]

@router.get("/functions/{function_id}")
async def get_function(function_id: int, db: Session = Depends(get_db)):
    """Get a function configuration by ID"""
    function = db.query(FunctionConfig).filter(FunctionConfig.id == function_id).first()
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")
    
    return {
        "id": function.id,
        "name": function.name,
        "description": function.description,
        "input_schema": json.loads(function.input_schema),
        "implementation_type": function.implementation_type,
        "implementation_config": json.loads(function.implementation_config),
        "is_active": function.is_active,
        "created_at": function.created_at,
        "updated_at": function.updated_at
    }

@router.post("/functions")
async def create_function(
    name: str = Form(...),
    description: str = Form(...),
    input_schema: str = Form(...),
    implementation_type: str = Form(...),
    implementation_config: str = Form(...),
    is_active: bool = Form(True),
    db: Session = Depends(get_db)
):
    """Create a new function configuration"""
    try:
        # Validate JSON schemas
        validate_json_schema(input_schema)
        validate_json_schema(implementation_config)
        
        # Check for existing function with same name
        existing = db.query(FunctionConfig).filter(FunctionConfig.name == name).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Function with name '{name}' already exists")
        
        # Create new function
        function = FunctionConfig(
            name=name,
            description=description,
            input_schema=input_schema,
            implementation_type=implementation_type,
            implementation_config=implementation_config,
            is_active=is_active
        )
        
        db.add(function)
        db.commit()
        db.refresh(function)
        
        return {"success": True, "function_id": function.id}
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.put("/functions/{function_id}")
async def update_function(
    function_id: int,
    name: str = Form(...),
    description: str = Form(...),
    input_schema: str = Form(...),
    implementation_type: str = Form(...),
    implementation_config: str = Form(...),
    is_active: bool = Form(True),
    db: Session = Depends(get_db)
):
    """Update an existing function configuration"""
    try:
        # Validate JSON schemas
        validate_json_schema(input_schema)
        validate_json_schema(implementation_config)
        
        # Get existing function
        function = db.query(FunctionConfig).filter(FunctionConfig.id == function_id).first()
        if not function:
            raise HTTPException(status_code=404, detail="Function not found")
        
        # Check for name conflict if name is changed
        if function.name != name:
            existing = db.query(FunctionConfig).filter(FunctionConfig.name == name).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"Function with name '{name}' already exists")
        
        # Update fields
        function.name = name
        function.description = description
        function.input_schema = input_schema
        function.implementation_type = implementation_type
        function.implementation_config = implementation_config
        function.is_active = is_active
        
        db.commit()
        
        return {"success": True, "function_id": function.id}
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.delete("/functions/{function_id}")
async def delete_function(function_id: int, db: Session = Depends(get_db)):
    """Delete a function configuration"""
    function = db.query(FunctionConfig).filter(FunctionConfig.id == function_id).first()
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")
    
    db.delete(function)
    db.commit()
    
    return {"success": True}