import json
import os
from pathlib import Path
from models import FunctionConfig
from database import init_db, SessionLocal

def create_initial_functions():
    """Create initial function configurations from seed data files"""
    db = SessionLocal()
    
    # Check if any functions already exist
    existing = db.query(FunctionConfig).count()
    if existing > 0:
        print(f"Found {existing} existing functions, skipping initialization")
        return
    
    # Load functions from JSON file
    seed_dir = Path(__file__).parent / "data" / "seed"
    functions_file = seed_dir / "functions.json"
    
    if not functions_file.exists():
        print(f"Warning: Seed file {functions_file} not found")
        return
    
    with open(functions_file, 'r') as f:
        functions_data = json.load(f)
    
    # Create functions from seed data
    for func_data in functions_data:
        # Convert input_schema and implementation_config to JSON strings if they aren't already
        input_schema = func_data.get('input_schema')
        if not isinstance(input_schema, str):
            input_schema = json.dumps(input_schema, indent=2)
            
        impl_config = func_data.get('implementation_config')
        if not isinstance(impl_config, str):
            impl_config = json.dumps(impl_config, indent=2)
        
        function = FunctionConfig(
            name=func_data.get('name'),
            description=func_data.get('description'),
            input_schema=input_schema,
            implementation_type=func_data.get('implementation_type'),
            implementation_config=impl_config
        )
        
        db.add(function)
        print(f"Created function: {func_data.get('name')}")
    
    db.commit()
    print(f"Added {len(functions_data)} functions from seed data")

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Creating initial functions...")
    create_initial_functions()
    print("Database initialization complete!")