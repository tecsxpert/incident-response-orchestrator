"""
Utility functions for the AI Service

This module contains common utility functions used across the service.
"""

import logging
from functools import wraps
from flask import request, jsonify

logger = logging.getLogger(__name__)


def require_json(f):
    """Decorator to ensure request has JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {'error': 'Request must be JSON'}, 400
        return f(*args, **kwargs)
    return decorated_function


def handle_errors(f):
    """Decorator to handle common errors gracefully"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f'Validation error: {e}')
            return {'error': str(e)}, 400
        except Exception as e:
            logger.error(f'Unexpected error: {e}', exc_info=True)
            return {'error': 'Internal server error'}, 500
    return decorated_function


def validate_required_fields(required_fields):
    """Decorator to validate required JSON fields"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return {'error': 'Request body is empty'}, 400
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return {
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }, 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
