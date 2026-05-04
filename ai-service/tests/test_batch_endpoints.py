"""
Pytest unit tests for batch processing endpoint.
Tests format, error handling, edge cases, and delay validation.

Test Coverage:
- 12+ test cases covering batch processing
- Sequential and parallel modes
- Item limit validation (max 20)
- Delay verification (100ms per item)
- Error handling and edge cases
"""

import pytest
import json
import time
from unittest.mock import patch


class TestBatchProcessSingleEndpoint:
    """Tests for POST /api/batch/process endpoint (8 tests)."""

    def test_valid_batch_with_single_item(self, test_client, mock_groq_instance):
        """Test 1: Single item batch processing returns success."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            payload = {
                'items': [
                    {
                        'id': 'item_1',
                        'content': 'Test incident content.',
                        'type': 'incident',
                        'priority': 'high'
                    }
                ]
            }
            response = test_client.post('/api/batch/process', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'completed'
            assert 'batch_id' in data
            assert len(data['results']) == 1
            assert data['results'][0]['status'] == 'success'

    def test_batch_with_maximum_20_items(self, test_client, mock_groq_instance):
        """Test 2: Batch with exactly 20 items (max limit) succeeds."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            items = [
                {
                    'id': f'item_{i}',
                    'content': f'Item {i} content.',
                    'type': 'log'
                }
                for i in range(20)
            ]
            payload = {'items': items}
            response = test_client.post('/api/batch/process', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['summary']['total_items'] == 20
            assert data['summary']['successful'] == 20

    def test_batch_exceeds_20_item_limit_returns_400(self, test_client):
        """Test 3: Batch with >20 items returns 400 error."""
        items = [
            {'id': f'item_{i}', 'content': f'Content {i}.'}
            for i in range(21)  # 21 items exceeds limit
        ]
        payload = {'items': items}
        response = test_client.post('/api/batch/process', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert '20' in data['error']

    def test_batch_missing_items_field_returns_400(self, test_client):
        """Test 4: Missing items field returns 400."""
        payload = {'someOtherField': []}
        response = test_client.post('/api/batch/process', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_batch_empty_items_list_returns_400(self, test_client):
        """Test 5: Empty items list returns 400."""
        payload = {'items': []}
        response = test_client.post('/api/batch/process', json=payload)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_batch_with_multiple_items(self, test_client, mock_groq_instance):
        """Test 6: Batch with 5 items processes successfully."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            items = [
                {
                    'id': f'item_{i}',
                    'content': f'Item {i} incident report.',
                    'type': 'report',
                    'priority': 'medium'
                }
                for i in range(5)
            ]
            payload = {'items': items}
            response = test_client.post('/api/batch/process', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['summary']['total_items'] == 5
            assert len(data['results']) == 5

    def test_batch_response_structure_complete(self, test_client, mock_groq_instance):
        """Test 7: Response has all required fields and structure."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            payload = {
                'items': [
                    {'id': 'test_1', 'content': 'Test content.'}
                ]
            }
            response = test_client.post('/api/batch/process', json=payload)
            
            data = json.loads(response.data)
            
            # Top-level fields
            assert 'status' in data
            assert 'batch_id' in data
            assert 'results' in data
            assert 'summary' in data
            assert 'metadata' in data
            
            # Results structure
            assert isinstance(data['results'], list)
            
            # Summary structure
            summary = data['summary']
            assert 'total_items' in summary
            assert 'successful' in summary
            assert 'failed' in summary
            assert 'total_time_ms' in summary
            assert 'average_time_per_item_ms' in summary
            assert 'completed_at' in summary
            
            # Metadata structure
            metadata = data['metadata']
            assert 'batch_size' in metadata
            assert 'max_batch_size' in metadata
            assert 'delay_per_item_ms' in metadata
            assert metadata['max_batch_size'] == 20

    def test_batch_item_with_missing_content_returns_error_status(self, test_client, mock_groq_instance):
        """Test 8: Item with empty content gets error status in results."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            items = [
                {'id': 'valid_1', 'content': 'Valid content.'},
                {'id': 'empty_1', 'content': ''},  # Empty content
                {'id': 'valid_2', 'content': 'Another valid item.'}
            ]
            payload = {'items': items}
            response = test_client.post('/api/batch/process', json=payload)
            
            data = json.loads(response.data)
            # Empty item should have error status
            empty_result = [r for r in data['results'] if r['id'] == 'empty_1'][0]
            assert empty_result['status'] == 'error'
            assert 'empty' in empty_result.get('error', '').lower()


class TestBatchProcessParallelEndpoint:
    """Tests for parallel batch processing (2 tests)."""

    def test_parallel_batch_processing_endpoint(self, test_client, mock_groq_instance):
        """Test 9: Parallel endpoint enables parallel processing."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            items = [
                {'id': f'item_{i}', 'content': f'Item {i}.'}
                for i in range(3)
            ]
            payload = {'items': items}
            response = test_client.post('/api/batch/process/parallel', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'completed'
            assert data['metadata']['parallel_processing'] == True

    def test_parallel_vs_sequential_timing(self, test_client, mock_groq_instance):
        """Test 10: Verify processing with delay is applied."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            items = [
                {'id': f'item_{i}', 'content': f'Item {i}.'}
                for i in range(3)
            ]
            payload = {'items': items}
            
            # Sequential processing should take at least 300ms (100ms * 3)
            start = time.time()
            response = test_client.post('/api/batch/process', json=payload)
            elapsed = (time.time() - start) * 1000  # Convert to ms
            
            data = json.loads(response.data)
            assert data['summary']['total_time_ms'] >= 300  # At least 3 items * 100ms


class TestBatchDelayAndMetrics:
    """Tests for delay and metrics (2 tests)."""

    def test_batch_respects_100ms_delay_per_item(self, test_client, mock_groq_instance):
        """Test 11: Each item has ~100ms delay applied."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            items = [
                {'id': f'item_{i}', 'content': f'Item {i}.'}
                for i in range(2)
            ]
            payload = {'items': items}
            response = test_client.post('/api/batch/process', json=payload)
            
            data = json.loads(response.data)
            # Each item has 100ms delay
            for result in data['results']:
                assert result['processing_time_ms'] == 100

    def test_batch_metadata_shows_correct_configuration(self, test_client, mock_groq_instance):
        """Test 12: Metadata shows correct batch configuration."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            payload = {
                'items': [{'id': 'test_1', 'content': 'Test.'}],
                'parallel': False
            }
            response = test_client.post('/api/batch/process', json=payload)
            
            data = json.loads(response.data)
            metadata = data['metadata']
            
            assert metadata['delay_per_item_ms'] == 100
            assert metadata['max_batch_size'] == 20
            assert metadata['parallel_processing'] == False
            assert 'max_workers' in metadata


class TestBatchErrorHandling:
    """Tests for error handling (2+ tests)."""

    def test_batch_with_invalid_json(self, test_client):
        """Test 13: Invalid JSON returns 400."""
        response = test_client.post(
            '/api/batch/process',
            data='invalid json',
            content_type='application/json'
        )
        
        assert response.status_code == 400

    def test_batch_status_endpoint_placeholder(self, test_client):
        """Test 14: Batch status endpoint returns not_found (async placeholder)."""
        response = test_client.get('/api/batch/status/batch_12345')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data


class TestBatchEdgeCases:
    """Tests for edge cases (2+ tests)."""

    def test_batch_with_optional_fields_omitted(self, test_client, mock_groq_instance):
        """Test 15: Items work with minimal required fields only."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            payload = {
                'items': [
                    {'content': 'Minimal item 1.'},
                    {'content': 'Minimal item 2.'}
                ]
            }
            response = test_client.post('/api/batch/process', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['summary']['successful'] == 2

    def test_batch_items_with_unicode_content(self, test_client, mock_groq_instance):
        """Test 16: Unicode content in items is handled correctly."""
        with patch('routes.batch.GroqClient', return_value=mock_groq_instance):
            payload = {
                'items': [
                    {'id': 'unicode_1', 'content': 'Security breach: 日本語テキスト 🔒'},
                    {'id': 'unicode_2', 'content': 'Incident: العربية النص العربي'},
                    {'id': 'emoji', 'content': 'Alert 🚨 with special chars ⚠️'}
                ]
            }
            response = test_client.post('/api/batch/process', json=payload)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['summary']['successful'] == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short', '-ra'])
