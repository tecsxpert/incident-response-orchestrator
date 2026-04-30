"""
Pytest unit tests for document analysis endpoints.
Tests format, error handling, and edge cases with mocked Groq responses.

Test Coverage:
- 10+ test cases covering single and bulk endpoints
- Error handling for invalid inputs
- Response format validation
- Severity and doc_type validation
- Edge cases (long content, limits, etc.)
"""

import pytest
import json
from unittest.mock import patch


class TestAnalyseSingleDocumentEndpoint:
    """Tests for POST /api/analyse/document endpoint (6 tests)."""

    def test_valid_document_returns_200_with_findings(self, test_client, mock_groq_instance):
        """Test 1: Valid document analysis returns 200 with analysis structure."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            payload = {
                'content': 'Security policy document with weak controls.',
                'doc_type': 'policy',
                'source': 'security_team',
                'priority': 'high'
            }
            response = test_client.post(
                '/api/analyse/document',
                json=payload,
                content_type='application/json'
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert 'analysis' in data
            assert 'generated_at' in data
            assert len(data['analysis']['findings']) > 0

    def test_missing_required_content_returns_400(self, test_client):
        """Test 2: Missing content field returns 400 error."""
        payload = {
            'doc_type': 'policy',
            'source': 'test'
        }
        response = test_client.post('/api/analyse/document', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'content' in data['error'].lower()

    def test_empty_content_returns_400(self, test_client):
        """Test 3: Empty content string returns 400 error."""
        payload = {'content': ''}
        response = test_client.post('/api/analyse/document', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_invalid_doc_type_returns_400(self, test_client):
        """Test 4: Invalid doc_type returns 400 error."""
        payload = {
            'content': 'Test content.',
            'doc_type': 'invalid_doc_type'
        }
        response = test_client.post('/api/analyse/document', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'doc_type' in data['error'].lower()

    def test_invalid_priority_returns_400(self, test_client):
        """Test 5: Invalid priority level returns 400 error."""
        payload = {
            'content': 'Test content.',
            'priority': 'super-urgent'  # Invalid
        }
        response = test_client.post('/api/analyse/document', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'priority' in data['error'].lower()

    def test_response_format_has_all_required_fields(self, test_client, mock_groq_instance):
        """Test 6: Response has all required fields and proper structure."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            payload = {'content': 'Test document.'}
            response = test_client.post('/api/analyse/document', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            # Verify top-level structure
            assert 'status' in data
            assert 'analysis' in data
            assert 'generated_at' in data
            assert 'metadata' in data
            
            # Verify analysis structure
            analysis = data['analysis']
            required_fields = [
                'document_title', 'summary', 'findings', 'key_insights',
                'risk_assessment', 'compliance_notes', 'metadata'
            ]
            for field in required_fields:
                assert field in analysis, f"Missing field: {field}"


class TestAnalyseBulkDocumentEndpoint:
    """Tests for POST /api/analyse/document/bulk endpoint (4 tests)."""

    def test_valid_bulk_analysis_returns_200(self, test_client, mock_groq_instance):
        """Test 7: Bulk analysis with valid documents returns 200."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            payload = {
                'documents': [
                    {'content': 'Doc 1 content.', 'doc_type': 'policy'},
                    {'content': 'Doc 2 content.', 'doc_type': 'log'},
                    {'content': 'Doc 3 content.', 'doc_type': 'alert'}
                ]
            }
            response = test_client.post('/api/analyse/document/bulk', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'completed'
            assert 'results' in data
            assert 'summary' in data
            assert len(data['results']) == 3

    def test_bulk_exceeds_10_document_limit_returns_400(self, test_client):
        """Test 8: Bulk request with >10 documents returns 400 (limit)."""
        payload = {
            'documents': [
                {'content': f'Document {i} content.'}
                for i in range(11)  # 11 documents exceeds limit
            ]
        }
        response = test_client.post('/api/analyse/document/bulk', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_bulk_empty_documents_list_returns_400(self, test_client):
        """Test 9: Empty documents list returns 400."""
        payload = {'documents': []}
        response = test_client.post('/api/analyse/document/bulk', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_bulk_missing_documents_field_returns_400(self, test_client):
        """Test 10: Missing documents field returns 400."""
        payload = {'someOtherField': []}
        response = test_client.post('/api/analyse/document/bulk', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestFindingsValidation:
    """Tests for findings structure and values (2 tests)."""

    def test_finding_has_all_required_fields(self, test_client, mock_groq_instance):
        """Test 11: Each finding has all required fields."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            payload = {'content': 'Test document.'}
            response = test_client.post('/api/analyse/document', json=payload)
            
            data = json.loads(response.data)
            findings = data['analysis']['findings']
            
            required_fields = [
                'finding_type', 'title', 'description', 'severity',
                'impact', 'recommendation'
            ]
            
            for finding in findings:
                for field in required_fields:
                    assert field in finding, f"Missing field in finding: {field}"
                    assert finding[field] is not None
                    assert len(str(finding[field])) > 0

    def test_severity_values_from_valid_set(self, test_client, mock_groq_instance):
        """Test 12: Severity values are from valid set."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            payload = {'content': 'Test document.'}
            response = test_client.post('/api/analyse/document', json=payload)
            
            data = json.loads(response.data)
            findings = data['analysis']['findings']
            
            valid_severities = ['critical', 'high', 'medium', 'low', 'informational']
            
            for finding in findings:
                assert finding['severity'] in valid_severities, \
                    f"Invalid severity: {finding['severity']}"


class TestDocumentTypeValidation:
    """Tests for document type validation (2 parametrized tests = 14 test cases)."""

    @pytest.mark.parametrize('doc_type', [
        'policy', 'log', 'alert', 'configuration', 'report',
        'memo', 'ticket', 'security_document', 'other'
    ])
    def test_all_valid_doc_types_accepted(self, test_client, mock_groq_instance, doc_type):
        """Test 13: All 9 valid document types are accepted."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            payload = {
                'content': 'Test document.',
                'doc_type': doc_type
            }
            response = test_client.post('/api/analyse/document', json=payload)
            
            assert response.status_code == 200, f"Failed for doc_type: {doc_type}"

    @pytest.mark.parametrize('invalid_type', [
        'invalid', 'unknown', 'security_type', 'document', 'text'
    ])
    def test_invalid_doc_types_rejected(self, test_client, invalid_type):
        """Test 14: Invalid document types are rejected with 400."""
        payload = {
            'content': 'Test.',
            'doc_type': invalid_type
        }
        response = test_client.post('/api/analyse/document', json=payload)
        
        assert response.status_code == 400, f"Should reject doc_type: {invalid_type}"


class TestEdgeCasesAndErrorHandling:
    """Tests for edge cases and error handling (2+ tests)."""

    def test_very_long_content_handled(self, test_client, mock_groq_instance):
        """Test 15: Very long document content is handled gracefully."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            # Create content much longer than typical 8000 char limit
            long_content = 'X' * 20000
            payload = {'content': long_content}
            
            response = test_client.post('/api/analyse/document', json=payload)
            
            # Should succeed (content will be truncated by GroqClient)
            assert response.status_code == 200

    def test_bulk_summary_has_all_counts(self, test_client, mock_groq_instance):
        """Test 16: Bulk response summary has all expected counts."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            payload = {
                'documents': [
                    {'content': 'Doc 1.'},
                    {'content': 'Doc 2.'},
                    {'content': 'Doc 3.'}
                ]
            }
            response = test_client.post('/api/analyse/document/bulk', json=payload)
            
            data = json.loads(response.data)
            summary = data['summary']
            
            # Verify summary structure
            assert 'total_documents' in summary
            assert 'successful' in summary
            assert 'failed' in summary
            assert 'completed_at' in summary
            
            # Verify counts match
            assert summary['total_documents'] == 3
            assert summary['successful'] == 3
            assert summary['failed'] == 0

    def test_default_parameters_used(self, test_client, mock_groq_instance):
        """Test 17: Default values used when optional parameters omitted."""
        with patch('routes.analyse.GroqClient', return_value=mock_groq_instance):
            # Only provide required content
            payload = {'content': 'Minimal document.'}
            
            response = test_client.post('/api/analyse/document', json=payload)
            
            # Should succeed with defaults for optional fields
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short', '-ra'])
