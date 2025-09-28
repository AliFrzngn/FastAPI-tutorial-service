"""
Central models module that imports all models to resolve circular dependencies.
This ensures that all models are loaded together and relationships work properly.
"""

# Import all models to ensure they are all registered with SQLAlchemy
from tasks.models import TaskModel
from users.models import UserModel

# Export all models for easy importing
__all__ = ["TaskModel", "UserModel"]
