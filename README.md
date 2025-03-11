# AI Factory

A flexible system for creating and managing AI function calls across different providers (Anthropic, Perplexity, Ollama) through a unified interface.

## Overview

AI Factory allows you to create, test, and execute functions with various AI providers through a configuration-driven system. It stores function definitions (including input schemas, implementation details, and AI prompts) as configurations in a database, which can be edited through the web interface.

This approach allows non-developers to modify how functions work by updating text configurations rather than changing code, making the system highly adaptable.

## Key Features

- **No-Code Function Creation**: Define new API endpoints through the web interface
- **Multiple Implementation Types**:
  - Claude API integration for AI-powered functions
  - Other provider integrations (Perplexity, Ollama)
  - Database queries for data operations
  - Python code for custom logic
- **Configurable Input Schemas**: Define expected input format using JSON Schema
- **REST API Endpoints**: Each function is automatically exposed as a REST endpoint
- **Modern Web Interface**: Manage functions through a responsive Svelte frontend

## Components

- **Backend**: FastAPI API (/backend)
- **Frontend**: Svelte UI (/frontend)

## Development

### Backend
```bash
cd backend
uv sync  # Install dependencies
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Running the Application

```bash
# Start the backend
./run_backend.sh

# Start the frontend 
./run_frontend.sh
```

Access the web interface at http://localhost:5173  
API documentation is available at http://localhost:8000/docs

## Integration with other services

Other applications can call AI Factory functions via its REST API:

```python
import requests

# Call a function
response = requests.post(
    "http://localhost:8000/api/functions/function_name",
    json={"inputs": {"param1": "value1", "param2": "value2"}}
)

result = response.json()
```

## Example: Car Repair Wiki Generation

The system includes a sample function for generating structured wiki articles from car repair messages that demonstrates the power of AI-driven function execution.