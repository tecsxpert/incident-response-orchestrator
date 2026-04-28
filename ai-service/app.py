"""Flask application entry point."""

from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
import logging
import os


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config=None):
    """Create Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    try:
        from routes.describe import describe_bp
        from routes.recommend import recommend_bp
        app.register_blueprint(describe_bp)
        app.register_blueprint(recommend_bp)
        logger.info("Registered describe and recommend blueprints")
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
                    "POST /api/describe/summary - Executive summary"
                ],
                "recommend": [
                    "POST /api/recommend - Action recommendations",
                    "POST /api/recommend/escalation - Escalation procedures",
                    "POST /api/recommend/remediation - Remediation plan"
                ],
                "health": [
                    "GET /health - Health check"
                ]
            },
            "framework": "MITRE ATT&CK / CVSS / NIST CSF"
        }), 200
    
    logger.info("Flask application created successfully")
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
