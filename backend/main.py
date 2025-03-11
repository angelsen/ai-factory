from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routers import functions, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize the database
    init_db()
    yield
    # Shutdown: cleanup resources if needed

# Use the lifespan context manager
app = FastAPI(
    title="AI Factory API", 
    description="Configuration-Driven AI Function System",
    lifespan=lifespan
)

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(functions.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {
        "message": "AI Factory API",
        "docs": "/docs",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
