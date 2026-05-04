"""Batch processing endpoint for concurrent item analysis with controlled delays."""

from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from prompts.templates import SYSTEM_PROMPT
from utils import require_json, handle_errors
import logging
from datetime import datetime, timezone
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
batch_bp = Blueprint("batch", __name__, url_prefix="/api/batch")

# Configuration
MAX_BATCH_SIZE = 20
PROCESSING_DELAY_MS = 100  # 100ms delay per item
MAX_WORKERS = 5  # Concurrent workers for parallel processing


def get_groq_client():
    """Get Groq client instance."""
    try:
        return GroqClient()
    except ValueError as e:
        raise ValueError(f"Groq client initialization failed: {str(e)}")


def process_single_item(item, index, groq_client):
    """
    Process a single batch item.
    
    Args:
        item: Item data with content, type, source, priority
        index: Position in batch
        groq_client: GroqClient instance
    
    Returns:
        Dict with processing result
    """
    try:
        # Apply processing delay (100ms per item)
        time.sleep(PROCESSING_DELAY_MS / 1000.0)
        
        # Extract fields with defaults
        content = item.get('content', '')
        item_type = item.get('type', 'generic')
        source = item.get('source', 'batch_processor')
        priority = item.get('priority', 'medium')
        item_id = item.get('id', f'item_{index}')
        
        if not content or not content.strip():
            return {
                'status': 'error',
                'index': index,
                'id': item_id,
                'error': 'Content is required and cannot be empty',
                'processed_at': datetime.now(timezone.utc).isoformat() + 'Z'
            }
        
        # Analyze content using GroqClient
        # For batch items, we can use a simplified analysis
        analysis = groq_client.analyze_document(
            content=content,
            doc_type=item_type,
            source=source,
            priority=priority
        )
        
        return {
            'status': 'success',
            'index': index,
            'id': item_id,
            'type': item_type,
            'analysis': analysis,
            'processed_at': datetime.now(timezone.utc).isoformat() + 'Z',
            'processing_time_ms': PROCESSING_DELAY_MS
        }
    
    except Exception as e:
        logger.error(f"Error processing batch item {index}: {str(e)}")
        return {
            'status': 'error',
            'index': index,
            'id': item.get('id', f'item_{index}'),
            'error': str(e),
            'processed_at': datetime.now(timezone.utc).isoformat() + 'Z'
        }


@batch_bp.route("/process", methods=["POST"])
@require_json
@handle_errors
def batch_process():
    """
    Process multiple items in a batch with controlled delays.
    
    Accepts up to 20 items, processes each with 100ms delay,
    returns results array with status for each item.
    
    Request body:
    {
        "items": [
            {
                "id": "item_1 (optional)",
                "content": "Item content (required)",
                "type": "incident|document|log|alert|other (optional, default: generic)",
                "source": "Source system (optional)",
                "priority": "low|medium|high|critical (optional)"
            },
            ...
        ],
        "parallel": false,
        "timeout": 300000
    }
    
    Returns:
    {
        "status": "completed",
        "batch_id": "batch_12345",
        "results": [
            {
                "status": "success",
                "index": 0,
                "id": "item_1",
                "type": "document",
                "analysis": {...},
                "processed_at": "ISO 8601",
                "processing_time_ms": 100
            },
            {
                "status": "error",
                "index": 1,
                "id": "item_2",
                "error": "Error message",
                "processed_at": "ISO 8601"
            }
        ],
        "summary": {
            "total_items": 2,
            "successful": 1,
            "failed": 1,
            "total_time_ms": 250,
            "completed_at": "ISO 8601"
        },
        "metadata": {
            "batch_size": 2,
            "max_batch_size": 20,
            "delay_per_item_ms": 100,
            "parallel_processing": false
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'items' not in data:
            return jsonify({'error': 'Missing required field: items'}), 400
        
        items = data.get('items', [])
        if not isinstance(items, list):
            return jsonify({'error': 'items must be an array'}), 400
        
        if len(items) == 0:
            return jsonify({'error': 'items array cannot be empty'}), 400
        
        if len(items) > MAX_BATCH_SIZE:
            return jsonify({
                'error': f'Batch size exceeds limit: {len(items)} > {MAX_BATCH_SIZE}'
            }), 400
        
        # Get optional parameters
        parallel = data.get('parallel', False)
        timeout_ms = data.get('timeout', 300000)  # 5 minute default
        
        # Generate batch ID
        batch_id = f"batch_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:-3]}"
        
        # Initialize GroqClient
        groq_client = get_groq_client()
        
        # Track processing time
        start_time = time.time()
        results = []
        
        if parallel:
            # Parallel processing with ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {
                    executor.submit(process_single_item, item, idx, groq_client): idx
                    for idx, item in enumerate(items)
                }
                
                for future in as_completed(futures):
                    try:
                        result = future.result(timeout=timeout_ms / 1000.0)
                        results.append(result)
                    except Exception as e:
                        idx = futures[future]
                        results.append({
                            'status': 'error',
                            'index': idx,
                            'id': items[idx].get('id', f'item_{idx}'),
                            'error': str(e),
                            'processed_at': datetime.now(timezone.utc).isoformat() + 'Z'
                        })
            
            # Sort results by index to maintain order
            results = sorted(results, key=lambda r: r.get('index', 0))
        else:
            # Sequential processing
            for idx, item in enumerate(items):
                result = process_single_item(item, idx, groq_client)
                results.append(result)
        
        # Calculate completion metrics
        end_time = time.time()
        total_time_ms = int((end_time - start_time) * 1000)
        
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = sum(1 for r in results if r['status'] == 'error')
        
        # Build response
        response = {
            'status': 'completed',
            'batch_id': batch_id,
            'results': results,
            'summary': {
                'total_items': len(items),
                'successful': successful,
                'failed': failed,
                'total_time_ms': total_time_ms,
                'average_time_per_item_ms': total_time_ms // len(items) if items else 0,
                'completed_at': datetime.now(timezone.utc).isoformat() + 'Z'
            },
            'metadata': {
                'batch_size': len(items),
                'max_batch_size': MAX_BATCH_SIZE,
                'delay_per_item_ms': PROCESSING_DELAY_MS,
                'parallel_processing': parallel,
                'max_workers': MAX_WORKERS if parallel else 1
            }
        }
        
        return jsonify(response), 200
    
    except ValueError as e:
        logger.error(f"Batch processing error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected batch processing error: {str(e)}")
        return jsonify({'error': f'Batch processing failed: {str(e)}'}), 500


@batch_bp.route("/process/parallel", methods=["POST"])
@require_json
@handle_errors
def batch_process_parallel():
    """
    Process items in parallel with same interface as /process.
    
    This is a convenience endpoint that automatically enables parallel processing.
    All parameters same as /process endpoint.
    """
    try:
        data = request.get_json()
        # Enable parallel processing
        data['parallel'] = True
        # Temporarily replace request data
        request._cached_json = (data, request.json_cache_key if hasattr(request, 'json_cache_key') else None)
        return batch_process()
    except Exception as e:
        logger.error(f"Parallel batch processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@batch_bp.route("/status/<batch_id>", methods=["GET"])
@handle_errors
def get_batch_status(batch_id):
    """
    Get status of a batch processing job (placeholder for async implementation).
    
    Args:
        batch_id: Batch ID to check status for
    
    Returns:
        Batch status and results (or polling information for async jobs)
    """
    # This is a placeholder for future async batch processing
    # In a production system, this would query a job queue/cache
    return jsonify({
        'status': 'not_found',
        'error': f'Batch {batch_id} not found. Status endpoint requires async job storage.',
        'note': 'Current implementation returns results synchronously in /process response'
    }), 404
