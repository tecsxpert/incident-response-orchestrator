"""
Routes module for AI Service

This module contains all the Flask blueprints for the API routes.
"""

from .describe import describe_bp
from .recommend import recommend_bp

__all__ = ['describe_bp', 'recommend_bp']
