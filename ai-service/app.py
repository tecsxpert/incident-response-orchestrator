"""
Incident Response Orchestrator - AI Service
Flask application entry point with blueprints registration
"""

from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
try:
    from routes.describe import describe_bp
    from routes.recommend import recommend_bp
    
    app.register_blueprint(describe_bp)
    app.register_blueprint(recommend_bp)
    logger.info('Blueprints registered successfully')
except ImportError as e:
    logger.error(f'Failed to import blueprints: {e}')


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return {
        'status': 'healthy',
        'service': 'incident-response-ai-service',
        'version': '1.0.0'
    }, 200


# Root endpoint
@app.route('/', methods=['GET'])
def index():
    """Root endpoint providing API information"""
    return {
        'name': 'Incident Response Orchestrator - AI Service',
        'version': '1.0.0',
        'description': 'AI-powered incident analysis and recommendations',
        'endpoints': {
            'health': '/health',
            'describe': '/api/describe',
            'recommend': '/api/recommend'
        }
    }, 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f'404 error: {error}')
    return {'error': 'Endpoint not found', 'status': 404}, 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f'500 error: {error}')
    return {'error': 'Internal server error', 'status': 500}, 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    logger.warning(f'400 error: {error}')
    return {'error': 'Bad request', 'status': 400}, 400


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    logger.info(f'Starting AI Service on {host}:{port} (debug={debug_mode})')
    app.run(debug=debug_mode, port=port, host=host, threaded=True)
