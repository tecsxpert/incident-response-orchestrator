# AI Service - Incident Response Orchestrator

Intelligent security incident analysis and response orchestration service powered by Groq's LLM API. This Flask-based microservice provides comprehensive incident analysis, automated recommendations, document security scanning, and batch processing capabilities for security incident response workflows.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Service](#running-the-service)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)

---

## Features

- **Incident Analysis**: Comprehensive security incident analysis using MITRE ATT&CK, CVSS, and NIST frameworks
- **Recommendation Engine**: Automated actionable recommendations for incident response
- **Document Analysis**: Security scanning of logs, policies, configurations, and alerts
- **Bulk Operations**: Process multiple documents in single request
- **Batch Processing**: Handle up to 20 items with controlled delays and optional parallel execution
- **Streaming Support**: Real-time incident analysis streaming with Server-Sent Events
- **Error Handling**: Comprehensive validation and error reporting
- **CORS Support**: Cross-origin resource sharing enabled
- **Production Ready**: Gunicorn-compatible with structured logging

---

## Prerequisites

### System Requirements

- **Python**: 3.9 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 8GB minimum (for ML models)
- **Storage**: 3GB+ (for ChromaDB and model cache)

### External Requirements

- **Groq API Key**: Free tier at https://console.groq.com/keys
  - Model: `llama-3.3-70b-versatile` (or compatible Groq model)
  - API Rate Limits: Varies by tier (free tier: ~30 requests/min)

### Recommended Tools

- **Virtual Environment**: `venv` or `conda`
- **Package Manager**: `pip` (comes with Python)
- **API Testing**: Postman, VS Code REST Client, or `curl`

---

## Installation

### 1. Clone and Navigate

```bash
git clone https://github.com/hemanthd4641/incident-response-orchestrator.git
cd incident-response-orchestrator/ai-service
```

### 2. Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux (Bash)**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies Overview**:
- `Flask 3.0.0` - Web framework
- `Flask-CORS 4.0.0` - Cross-origin support
- `groq 0.9.0` - Groq API client
- `python-dotenv 1.0.0` - Environment configuration
- `chromadb 0.4.21` - Vector database for RAG
- `sentence-transformers 2.2.2` - Embeddings
- `torch 2.1.2` - ML framework
- `transformers 4.42.3` - Transformer models
- `gunicorn 21.2.0` - WSGI server (production)

### 4. Verify Installation

```bash
# Check Python version
python --version

# Verify all packages installed
pip list | findstr Flask groq chromadb
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `ai-service` directory with the following variables:

```bash
# Flask Configuration
FLASK_ENV=development              # Options: development, production, testing
FLASK_PORT=5000                    # Port number (default: 5000)

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key     # Required: Get from https://console.groq.com/keys
GROQ_MODEL=llama-3.3-70b-versatile # LLM model (default: mixtral-8x7b-32768)
```

### Example Configurations

**Development Environment** (`.env.development`):
```bash
FLASK_ENV=development
FLASK_PORT=5000
GROQ_API_KEY=gsk_your_test_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

**Production Environment** (`.env.production`):
```bash
FLASK_ENV=production
FLASK_PORT=5000
GROQ_API_KEY=gsk_your_production_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Getting Your Groq API Key

1. Visit https://console.groq.com/keys
2. Sign up or log in with your account
3. Create a new API key
4. Copy the key and add to `.env` file
5. **Important**: Never commit `.env` to version control

### Configuration File (`config.py`)

The application loads configuration based on `FLASK_ENV`:

- **Development**: `DevelopmentConfig` - DEBUG=True, TESTING=False
- **Production**: `ProductionConfig` - DEBUG=False, TESTING=False
- **Testing**: `TestingConfig` - DEBUG=True, TESTING=True

---

## Running the Service

### Development Mode

**Start with Flask development server** (auto-reload enabled):

```bash
python app.py
```

Output:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
* WARNING: This is a development server. Do not use it in production.
```

### Production Mode

**Using Gunicorn** (for production deployment):

```bash
# Single worker
gunicorn --bind 0.0.0.0:5000 --workers 1 app:create_app

# Multiple workers (recommended for production)
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:create_app

# With logging
gunicorn --bind 0.0.0.0:5000 --workers 4 --access-logfile - --error-logfile - app:create_app
```

### Health Check

Once running, verify the service is operational:

```bash
curl http://localhost:5000/
```

Response:
```json
{"error": "Not found"}
```

This is expected (404 for root path). The service is running if you get a JSON response.

### Service Logs

Logs are printed to stdout with format:
```
2026-05-04 10:30:45,123 - flask.app - INFO - Registered describe, recommend, analyse, and batch blueprints
```

Enable debug logging by setting `FLASK_ENV=development`.

---

## API Endpoints

### Base URL

All endpoints use the base URL: `http://localhost:5000/api`

### Response Format

All endpoints return JSON with consistent structure:

**Success Response (200-201)**:
```json
{
  "status": "success",
  "data": {},
  "generated_at": "2026-05-04T10:30:45.123456Z",
  "metadata": {}
}
```

**Error Response (400-500)**:
```json
{
  "error": "Error message",
  "details": "Additional details"
}
```

---

## Endpoints Reference

### 1. POST /api/describe - Analyze Incident

Analyzes a security incident with professional assessment using MITRE ATT&CK and NIST frameworks.

**Endpoint**: `POST /api/describe`

**Request Body**:
```json
{
  "description": "Detailed incident description (required)",
  "title": "Incident Title (optional)",
  "context": "Additional context (optional)",
  "severity_hint": "Severity level hint (optional)"
}
```

**Query Parameters**: None

**Headers Required**:
- `Content-Type: application/json`

**Response** (200):
```json
{
  "status": "success",
  "title": "Ransomware Attack - Finance Department",
  "analysis": "Multi-section comprehensive analysis covering indicators, MITRE ATT&CK tactics, severity assessment, and recommended response...",
  "generated_at": "2026-05-04T10:30:45.123456Z",
  "metadata": {
    "model_used": "llama-3.3-70b-versatile",
    "analysis_type": "comprehensive_incident_assessment",
    "framework": "MITRE ATT&CK / CVSS / NIST"
  }
}
```

**Error Response** (400):
```json
{
  "error": "Missing required field: description"
}
```

**Status Codes**:
- `200 OK` - Analysis successful
- `400 Bad Request` - Missing or invalid input
- `500 Internal Server Error` - Groq API or service error

---

### 2. POST /api/describe/generate-report-stream - Streaming Analysis

Streams incident analysis in real-time using Server-Sent Events (SSE).

**Endpoint**: `POST /api/describe/generate-report-stream`

**Request Body**:
```json
{
  "description": "Detailed incident description (required)",
  "title": "Incident Title (optional)",
  "context": "Additional context (optional)"
}
```

**Response Headers**:
- `Content-Type: text/event-stream`
- `Cache-Control: no-cache`
- `Connection: keep-alive`

**Response Stream** (200):
```
data: [SECTION 1] Incident Overview...
data: [SECTION 2] Technical Analysis...
data: [SECTION 3] Timeline...
```

**Error Response** (400):
```json
{
  "error": "Description is required"
}
```

**Status Codes**:
- `200 OK` - Stream started (text/event-stream)
- `400 Bad Request` - Missing required fields
- `500 Internal Server Error` - Stream generation failed

**Usage Notes**:
- Connection stays open until all sections complete
- Client should read events until connection closes
- Each event contains a section of the analysis

---

### 3. POST /api/recommend - Get Incident Recommendations

Generates 3 actionable recommendations for incident response based on incident type and severity.

**Endpoint**: `POST /api/recommend`

**Request Body**:
```json
{
  "incident_type": "ransomware",
  "severity": "critical",
  "description": "Ransomware detected on file servers..."
}
```

**Incident Types**:
- `ransomware`
- `data_exfiltration`
- `insider_threat`
- `sql_injection`
- `phishing`
- `apt` (Advanced Persistent Threat)
- `ddos` (Distributed Denial of Service)
- `malware`
- `other`

**Severity Levels**:
- `critical`
- `high`
- `medium`
- `low`

**Response** (200):
```json
{
  "status": "success",
  "incident_type": "ransomware",
  "severity": "critical",
  "recommendations": [
    {
      "action_type": "isolate_systems",
      "description": "Immediately disconnect affected systems from network to prevent spread...",
      "priority": 1
    },
    {
      "action_type": "reset_credentials",
      "description": "Reset all domain admin credentials and force re-authentication...",
      "priority": 1
    },
    {
      "action_type": "enable_mfa",
      "description": "Enable multi-factor authentication on critical systems...",
      "priority": 2
    }
  ],
  "generated_at": "2026-05-04T10:30:45.123456Z",
  "metadata": {
    "model_used": "llama-3.3-70b-versatile",
    "response_type": "structured_action_recommendations",
    "recommendation_count": 3,
    "framework": "NIST Incident Response"
  }
}
```

**Error Response** (400):
```json
{
  "error": "Missing required field: incident_type"
}
```

**Status Codes**:
- `200 OK` - Recommendations generated
- `400 Bad Request` - Missing or invalid fields
- `500 Internal Server Error` - Groq API error

---

### 4. POST /api/analyse/document - Analyze Single Document

Analyzes a single document (log, policy, alert, configuration) for security insights and risks.

**Endpoint**: `POST /api/analyse/document`

**Request Body**:
```json
{
  "content": "Full document text (required)",
  "doc_type": "log",
  "source": "syslog server",
  "priority": "high"
}
```

**Document Types**:
- `security_document` (default)
- `policy`
- `log`
- `alert`
- `configuration`
- `report`
- `memo`
- `other`

**Priority Levels**:
- `low`
- `medium` (default)
- `high`
- `critical`

**Response** (200):
```json
{
  "status": "success",
  "analysis": {
    "document_title": "Web Server Access Logs - 2026-05-04",
    "summary": "Analysis of 100 log entries from web server, identifying 3 suspicious patterns...",
    "findings": [
      {
        "finding_type": "threat",
        "title": "SQL Injection Attempts",
        "description": "Multiple POST requests contain SQL syntax...",
        "severity": "critical",
        "impact": "Potential database compromise",
        "recommendation": "Block IPs and review database logs",
        "references": "OWASP Top 10 - A03:2021 Injection"
      }
    ],
    "key_insights": [
      {
        "insight": "10 requests from single IP (192.168.1.100)",
        "significance": "Possible coordinated attack"
      }
    ],
    "risk_assessment": {
      "overall_risk_level": "high",
      "primary_threats": ["SQL Injection", "Brute Force"],
      "critical_gaps": ["Input validation", "Rate limiting"],
      "immediate_actions_required": ["Block IPs", "Review logs"],
      "business_impact": "Potential data breach affecting customer records"
    },
    "compliance_notes": {
      "frameworks_applicable": ["NIST", "CIS", "SOC 2"],
      "gaps_identified": ["Logging retention", "Audit trail"],
      "recommendations": "Implement centralized logging solution"
    },
    "metadata": {
      "analyzed_at": "2026-05-04T10:30:45.123456Z",
      "analysis_confidence": "high",
      "sections_reviewed": 5,
      "findings_count": 3
    }
  },
  "generated_at": "2026-05-04T10:30:45.123456Z",
  "metadata": {
    "model_used": "llama-3.3-70b-versatile",
    "analysis_type": "document_security_analysis",
    "doc_type": "log",
    "source": "syslog server"
  }
}
```

**Error Response** (400):
```json
{
  "error": "Missing required field: content"
}
```

**Status Codes**:
- `200 OK` - Analysis successful
- `400 Bad Request` - Missing required fields
- `500 Internal Server Error` - Groq API error

**Content Limits**:
- Maximum content size: 8000 characters (longer content is truncated)
- Minimum content size: 1 character (non-empty required)

---

### 5. POST /api/analyse/document/bulk - Bulk Analyze Documents

Analyzes multiple documents in a single request (up to 10 documents).

**Endpoint**: `POST /api/analyse/document/bulk`

**Request Body**:
```json
{
  "documents": [
    {
      "content": "Document 1 text",
      "doc_type": "log",
      "source": "server1"
    },
    {
      "content": "Document 2 text",
      "doc_type": "policy",
      "source": "compliance"
    }
  ]
}
```

**Response** (200):
```json
{
  "status": "success",
  "bulk_analysis_id": "bulk_20260504_103045_abc123",
  "results": [
    {
      "index": 0,
      "status": "success",
      "analysis": {
        "document_title": "...",
        "summary": "...",
        "findings": []
      }
    },
    {
      "index": 1,
      "status": "success",
      "analysis": {}
    }
  ],
  "summary": {
    "total_documents": 2,
    "successful_analyses": 2,
    "failed_analyses": 0,
    "total_findings": 5
  },
  "generated_at": "2026-05-04T10:30:45.123456Z",
  "metadata": {
    "model_used": "llama-3.3-70b-versatile",
    "bulk_analysis": true,
    "document_count": 2,
    "analysis_type": "bulk_document_analysis"
  }
}
```

**Error Response** (400):
```json
{
  "error": "Bulk size exceeds limit: 11 > 10"
}
```

**Status Codes**:
- `200 OK` - Bulk analysis completed (may include partial failures)
- `400 Bad Request` - Invalid request (exceeds limit, missing documents)
- `500 Internal Server Error` - Service error

**Limits**:
- Maximum documents per request: 10
- Each document limited to 8000 characters

---

### 6. POST /api/batch/process - Batch Process Items

Processes up to 20 items in parallel or sequential mode with 100ms delay per item.

**Endpoint**: `POST /api/batch/process`

**Request Body**:
```json
{
  "items": [
    {
      "id": "item_1",
      "content": "Item content",
      "type": "document",
      "source": "batch_system",
      "priority": "high"
    }
  ],
  "parallel": false,
  "timeout": 300000
}
```

**Parameters**:
- `items` (required): Array of items to process
- `parallel` (optional): Boolean, default `false` - Enable parallel processing
- `timeout` (optional): Integer (ms), default `300000` (5 min) - Processing timeout

**Item Properties**:
- `id` (optional): Unique identifier for the item
- `content` (required): Item content to analyze
- `type` (optional): Item type (incident, document, log, alert, other)
- `source` (optional): Source system
- `priority` (optional): Priority level (low, medium, high, critical)

**Response** (200):
```json
{
  "status": "completed",
  "batch_id": "batch_20260504103045789",
  "results": [
    {
      "status": "success",
      "index": 0,
      "id": "item_1",
      "type": "document",
      "analysis": {
        "document_title": "...",
        "summary": "...",
        "findings": []
      },
      "processed_at": "2026-05-04T10:30:45.123456Z",
      "processing_time_ms": 100
    }
  ],
  "summary": {
    "total_items": 1,
    "successful": 1,
    "failed": 0,
    "total_time_ms": 150,
    "average_time_per_item_ms": 150,
    "completed_at": "2026-05-04T10:30:45.123456Z"
  },
  "metadata": {
    "batch_size": 1,
    "max_batch_size": 20,
    "delay_per_item_ms": 100,
    "parallel_processing": false,
    "max_workers": 1
  }
}
```

**Error Response** (400):
```json
{
  "error": "Batch size exceeds limit: 25 > 20"
}
```

**Status Codes**:
- `200 OK` - Batch completed (may include item-level failures)
- `400 Bad Request` - Invalid request (exceeds limits, missing items)
- `500 Internal Server Error` - Service error

**Processing Details**:
- Each item gets 100ms processing delay
- Parallel mode uses ThreadPoolExecutor with max 5 workers
- Sequential mode processes items one at a time
- Order is preserved in results (sorted by index)
- Individual item errors don't fail entire batch

**Limits**:
- Maximum items per batch: 20
- Delay per item: 100ms (configurable)
- Maximum workers: 5 (parallel mode)
- Default timeout: 5 minutes

---

## Usage Examples

### Using curl

#### Example 1: Analyze an Incident

```bash
curl -X POST http://localhost:5000/api/describe \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ransomware Detected",
    "description": "Ransomware detected on file servers affecting 50GB of data",
    "severity_hint": "critical"
  }'
```

#### Example 2: Get Recommendations

```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "incident_type": "ransomware",
    "severity": "critical",
    "description": "Multiple file extensions encrypted with .locked extension"
  }'
```

#### Example 3: Analyze a Document

```bash
curl -X POST http://localhost:5000/api/analyse/document \
  -H "Content-Type: application/json" \
  -d '{
    "content": "2026-05-04 10:15:23 ERROR SQL injection attempt detected in POST parameter",
    "doc_type": "log",
    "source": "web_server",
    "priority": "critical"
  }'
```

#### Example 4: Bulk Analyze Documents

```bash
curl -X POST http://localhost:5000/api/analyse/document/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {"content": "Log entry 1", "doc_type": "log"},
      {"content": "Log entry 2", "doc_type": "log"}
    ]
  }'
```

#### Example 5: Batch Process Items

```bash
curl -X POST http://localhost:5000/api/batch/process \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"id": "item_1", "content": "Suspicious activity in logs", "type": "log"}
    ],
    "parallel": false,
    "timeout": 300000
  }'
```

### Using Python

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Analyze incident
response = requests.post(
    f"{BASE_URL}/describe",
    json={
        "description": "Ransomware attack detected",
        "severity_hint": "critical"
    }
)
print(json.dumps(response.json(), indent=2))

# Get recommendations
response = requests.post(
    f"{BASE_URL}/recommend",
    json={
        "incident_type": "ransomware",
        "severity": "critical",
        "description": "Files encrypted with .locked extension"
    }
)
print(json.dumps(response.json(), indent=2))

# Stream analysis
response = requests.post(
    f"{BASE_URL}/describe/generate-report-stream",
    json={"description": "Incident description"},
    stream=True
)
for event in response.iter_lines():
    if event:
        print(event.decode())
```

### Using JavaScript/Node.js

```javascript
const BASE_URL = 'http://localhost:5000/api';

// Analyze incident
const response = await fetch(`${BASE_URL}/describe`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    description: 'Security incident description',
    severity_hint: 'high'
  })
});

const data = await response.json();
console.log(data);

// Stream analysis
const streamResponse = await fetch(`${BASE_URL}/describe/generate-report-stream`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    description: 'Incident description'
  })
});

const reader = streamResponse.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(new TextDecoder().decode(value));
}
```

---

## Testing

### Run All Tests

```bash
# With verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=routes --cov=services

# Specific test file
pytest tests/test_analyse_endpoints.py -v

# Specific test class
pytest tests/test_analyse_endpoints.py::TestAnalyseSingleDocumentEndpoint -v

# Specific test
pytest tests/test_analyse_endpoints.py::TestAnalyseSingleDocumentEndpoint::test_valid_document_returns_200_with_findings -v
```

### Test Structure

```
tests/
├── conftest.py                    # Pytest fixtures and configuration
├── test_analyse_endpoints.py      # Document analysis tests (29 tests)
└── test_batch_endpoints.py        # Batch processing tests (16 tests)
```

### Test Coverage

- **Document Analysis**: 29 tests
  - Single document analysis
  - Bulk analysis (up to 10 documents)
  - Document type validation
  - Edge cases and error handling

- **Batch Processing**: 16 tests
  - Single and multiple item processing
  - Batch size limits (max 20)
  - Delay verification (100ms per item)
  - Sequential and parallel modes
  - Error handling and timeouts

### Running Tests with Mocking

All tests use mocked Groq API responses to avoid external dependencies:

```bash
# Tests run with mock GroqClient
pytest tests/test_analyse_endpoints.py::TestAnalyseSingleDocumentEndpoint::test_valid_document_returns_200_with_findings -v -s

# Output shows test execution with mocked responses
# PASSED - No actual Groq API calls made
```

---

## Architecture

### Service Structure

```
ai-service/
├── app.py                         # Flask application entry point
├── config.py                      # Configuration management
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (local)
├── .env.development              # Development configuration
│
├── routes/                        # API endpoints (blueprints)
│   ├── describe.py               # Incident analysis endpoints
│   ├── recommend.py              # Recommendation endpoints
│   ├── analyse.py                # Document analysis endpoints
│   └── batch.py                  # Batch processing endpoint
│
├── services/                      # Business logic
│   └── groq_client.py            # Groq API wrapper
│
├── prompts/                       # AI prompt templates
│   └── templates.py              # Prompt engineering
│
├── utils.py                       # Utility functions and decorators
├── documents/                     # Sample documents for RAG
├── chroma_data/                   # Vector database storage
│
└── tests/                         # Test suite
    ├── conftest.py               # Pytest configuration
    ├── test_analyse_endpoints.py # Analysis tests
    └── test_batch_endpoints.py   # Batch tests
```

### Request Flow

```
HTTP Request
    ↓
Flask Route Handler (@describe_bp.route)
    ↓
Validation (@require_json, @validate_required_fields)
    ↓
Error Handling (@handle_errors decorator)
    ↓
Business Logic (analyze_incident, recommend_actions, etc.)
    ↓
GroqClient Call (groq.client.chat)
    ↓
Response Parsing & Formatting
    ↓
JSON Response (200/400/500)
```

### Deployment Architecture

**Development**:
```
Client → Flask Dev Server (auto-reload)
        ↓
       Groq API
```

**Production**:
```
Client → Gunicorn (4 workers) → Flask App
                                    ↓
                                 Groq API
```

---

## Troubleshooting

### Issue: "No module named 'groq'"

**Solution**:
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import groq; print(groq.__version__)"
```

### Issue: "GROQ_API_KEY not found"

**Solution**:
1. Check `.env` file exists in `ai-service/` directory
2. Verify GROQ_API_KEY is set correctly
3. Ensure `.env` is not in `.gitignore` for local development

```bash
# Check environment variable
echo $env:GROQ_API_KEY  # PowerShell
echo $GROQ_API_KEY      # Bash
```

### Issue: "Connection refused" (Can't reach service)

**Solution**:
```bash
# Check if service is running
curl http://localhost:5000/

# Check port in use
netstat -ano | findstr :5000  # Windows PowerShell
lsof -i :5000                 # macOS/Linux

# Change port in .env
FLASK_PORT=5001
```

### Issue: "Timeout waiting for response"

**Solution**:
1. Check Groq API status: https://status.groq.com
2. Verify API rate limits not exceeded
3. Increase timeout in batch requests

```json
{
  "items": [...],
  "timeout": 600000
}
```

### Issue: "Model not available"

**Solution**:
1. List available models:
   ```bash
   # Use Groq API to list models
   curl -s -H "Authorization: Bearer $GROQ_API_KEY" \
        https://api.groq.com/openai/v1/models
   ```

2. Update `.env` with available model:
   ```bash
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

### Issue: Tests failing with mock errors

**Solution**:
```bash
# Run tests with debug output
pytest tests/ -v -s

# Check conftest.py fixtures loaded
pytest tests/ --fixtures

# Run specific test with traceback
pytest tests/test_analyse_endpoints.py::TestAnalyseSingleDocumentEndpoint -v --tb=long
```

### Issue: High memory usage

**Solution**:
1. ChromaDB and models consume significant RAM
2. Monitor with:
   ```bash
   # Windows
   Get-Process python
   
   # macOS/Linux
   ps aux | grep python
   ```

3. Reduce model cache:
   ```bash
   # Clear cache directory
   rm -rf ~/.cache/huggingface
   ```

### Issue: "Cross-Origin Request Blocked"

**Solution**:
- CORS is enabled by default
- Verify requests include proper headers:
  ```bash
  curl -H "Origin: http://localhost:3000" \
       -H "Content-Type: application/json" \
       http://localhost:5000/api/describe
  ```

---

## Performance Optimization

### For Production

1. **Use Gunicorn with multiple workers**:
   ```bash
   gunicorn --workers 4 --threads 2 --worker-class gthread app:create_app
   ```

2. **Enable connection pooling** (update `groq_client.py`):
   ```python
   session = requests.Session()
   session.headers.update({"Authorization": f"Bearer {api_key}"})
   ```

3. **Cache model embeddings** in ChromaDB

4. **Monitor with logging**:
   ```bash
   gunicorn --access-logfile logs/access.log \
            --error-logfile logs/error.log app:create_app
   ```

### Batch Processing Optimization

```python
# Use parallel processing for larger batches
{
  "items": [...],  # Up to 20 items
  "parallel": true,  # Enable parallel mode
  "timeout": 600000
}
```

---

## Support & Documentation

- **Groq API Docs**: https://console.groq.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **ChromaDB**: https://docs.trychroma.com/
- **Project Repository**: https://github.com/hemanthd4641/incident-response-orchestrator

---

**Last Updated**: May 4, 2026  
**Service Version**: 1.0.0  
**Python Version**: 3.9+
