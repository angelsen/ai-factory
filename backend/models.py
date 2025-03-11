from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from database import Base

class FunctionConfig(Base):
    __tablename__ = "function_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    input_schema = Column(Text)  # JSON schema as text
    implementation_type = Column(String)  # "anthropic", "perplexity", "ollama", "database_query", "python_code"
    implementation_config = Column(Text)  # JSON config as text
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)