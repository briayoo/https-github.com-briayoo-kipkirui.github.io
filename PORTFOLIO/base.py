"""
Base configuration and utilities
Contains base classes and utility functions
"""

from abc import ABC, abstractmethod
import json
from datetime import datetime

class BaseModel(ABC):
    """Abstract base model with common functionality"""
    
    @abstractmethod
    def to_dict(self):
        """Convert model instance to dictionary"""
        pass
    
    def to_json(self):
        """Convert model instance to JSON"""
        return json.dumps(self.to_dict(), default=str)

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps"""
    
    created_at = None
    updated_at = None
    
    def set_timestamps(self):
        """Set timestamps for new instances"""
        now = datetime.utcnow()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now

class SerializerMixin:
    """Mixin for serialization functionality"""
    
    def serialize(self):
        """Serialize object to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ConfigBase:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key-here'