"""Flask application entry point."""

from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
import logging
import os
import atexit


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global cache for pre-loaded models
_embedding_model = None
_redis_cache = None


def _preload_models():
    """Pre-load embedding model and initialize cache at startup."""
    global _embedding_model, _redis_cache
    
    try:
        # Pre-load sentence-transformers embedding model
        logger.info("Pre-loading sentence-transformers embedding model...")
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("✓ Embedding model loaded successfully")
    except Exception as e:
        logger.warning(f"Failed to pre-load embedding model: {str(e)}")
        _embedding_model = None
    
    try:
        # Initialize Redis cache
        logger.info("Initializing Redis cache...")
        import redis
        _redis_cache = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True
        )
        # Test connection
        _redis_cache.ping()
        logger.info("✓ Redis cache initialized and connected")
    except Exception as e:
        logger.info(f"Redis cache not available (optional): {str(e)}")
        _redis_cache = None


def get_embedding_model():
    """Get pre-loaded embedding model."""
    return _embedding_model


def get_redis_cache():
    """Get Redis cache instance."""
    return _redis_cache


def create_app(config=None):
    """Create Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app)
    
    # Pre-load models and initialize cache
    _preload_models()
    
    # Register blueprints
    try:
        from routes.describe import describe_bp
        from routes.recommend import recommend_bp
        from routes.analyse import analyse_bp
        from routes.batch import batch_bp
        app.register_blueprint(describe_bp)
        app.register_blueprint(recommend_bp)
        app.register_blueprint(analyse_bp)
        app.register_blueprint(batch_bp)
        logger.info("Registered describe, recommend, analyse, and batch blueprints")
    except Exception as e:
        logger.error(f"Failed to register blueprints: {str(e)}")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400
    
    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy"}), 200
    
    # Info endpoint
    @app.route("/", methods=["GET"])
    def info():
        return jsonify({
            "service": "incident-response-ai",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "describe": [
                    "POST /api/describe - Comprehensive incident analysis",
                    "POST /api/describe/similar - Find similar incidents",
                    "POST /api/describe/summary - Executive summary",
                    "POST /api/describe/generate-report - Generate structured report",
                    "POST /api/describe/generate-report-stream - Stream report tokens (SSE)"
                ],
                "recommend": [
                    "POST /api/recommend - Action recommendations",
                    "POST /api/recommend/escalation - Escalation procedures",
                    "POST /api/recommend/remediation - Remediation plan"
                ],
                "analyse": [
                    "POST /api/analyse/document - Analyze document for insights and risks",
                    "POST /api/analyse/document/bulk - Batch analyze multiple documents"
                ],
                "batch": [
                    "POST /api/batch/process - Batch process up to 20 items with 100ms delay",
                    "POST /api/batch/process/parallel - Parallel batch processing",
                    "GET /api/batch/status/<batch_id> - Get batch processing status"
                ],
                "health": [
                    "GET /health - Health check"
                ]
            },
            "framework": "MITRE ATT&CK / CVSS / NIST CSF",
            "features": ["incident_analysis", "structured_recommendations", "report_generation", "streaming_reports", "document_analysis", "batch_processing"]
        }), 200
    
    logger.info("Flask application created successfully")
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
