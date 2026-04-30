"""
Pytest configuration and fixtures for analyse endpoint tests.
Sets up mocking for external dependencies.
"""

import sys
import pytest
from unittest.mock import MagicMock

# Mock external modules before any imports
sys.modules['groq'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['chromadb'] = MagicMock()

# Set environment variables
import os
os.environ['GROQ_API_KEY'] = 'test-key-12345'


@pytest.fixture
def mock_groq_instance():
    """Provide a mocked GroqClient instance."""
    mock = MagicMock()
    mock.analyze_document.return_value = {
        'document_title': 'Test Document',
        'summary': 'Test summary',
        'findings': [
            {
                'finding_type': 'vulnerability',
                'title': 'Test Finding',
                'description': 'Test description',
                'severity': 'high',
                'impact': 'Test impact',
                'recommendation': 'Test recommendation',
                'references': 'TEST-001'
            }
        ],
        'key_insights': [
            {
                'insight': 'Test insight',
                'significance': 'Test significance'
            }
        ],
        'risk_assessment': {
            'overall_risk_level': 'high',
            'primary_threats': ['threat1', 'threat2'],
            'critical_gaps': ['gap1', 'gap2'],
            'immediate_actions_required': ['action1'],
            'business_impact': 'Test impact'
        },
        'compliance_notes': {
            'frameworks_applicable': ['NIST', 'GDPR'],
            'gaps_identified': ['gap1'],
            'recommendations': 'Test recommendations'
        },
        'metadata': {
            'analyzed_at': '2024-01-15T10:00:00Z',
            'analysis_confidence': 'high',
            'sections_reviewed': 3,
            'findings_count': 1
        }
    }
    return mock


@pytest.fixture
def flask_app():
    """Provide Flask test app."""
    from app import app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def test_client(flask_app):
    """Provide Flask test client."""
    return flask_app.test_client()
