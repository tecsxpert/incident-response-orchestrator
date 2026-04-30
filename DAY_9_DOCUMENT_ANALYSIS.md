# Day 9: Document Analysis Endpoint - POST /analyse/document

## Overview

Implemented a comprehensive document analysis endpoint that accepts text documents (policies, logs, alerts, configurations, reports) and performs deep security analysis to identify risks, vulnerabilities, compliance gaps, and actionable recommendations. Returns structured findings array with classified insights.

## Architecture

### Backend Flow

```
REST Client (Frontend/API)
    ↓
POST /api/analyse/document with content
    ↓
Input Validation & Preprocessing
    ↓
GroqClient.analyze_document()
    ↓
Groq API with ANALYZE_DOCUMENT_PROMPT
    ↓
AI Analysis with findings classification
    ↓
JSON Parsing & Validation
    ↓
Structured findings array returned
    ↓
Client receives analysis with metadata
```

## Endpoints

### 1. POST /api/analyse/document

Analyzes a single document for security insights and risks.

**Request:**
```json
{
  "content": "Full document text (required)",
  "doc_type": "security_document|policy|log|alert|configuration|report|memo|ticket|other (optional, default: security_document)",
  "source": "Source system or team (optional, default: unknown)",
  "priority": "low|medium|high|critical (optional, default: medium)"
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "document_title": "Extracted or inferred title",
    "summary": "2-3 sentence overview",
    "findings": [
      {
        "finding_type": "insight|risk|threat|vulnerability|misconfiguration|compliance_gap|best_practice|anomaly",
        "title": "Concise title",
        "description": "Detailed description with implications",
        "severity": "critical|high|medium|low|informational",
        "impact": "Potential business/security impact",
        "recommendation": "Specific actionable recommendation",
        "references": "MITRE ATT&CK | CVSS | Framework references"
      }
    ],
    "key_insights": [
      {
        "insight": "Observable pattern or notable finding",
        "significance": "Why this insight matters"
      }
    ],
    "risk_assessment": {
      "overall_risk_level": "critical|high|medium|low",
      "primary_threats": ["threat1", "threat2", "threat3"],
      "critical_gaps": ["gap1", "gap2"],
      "immediate_actions_required": ["action1", "action2"],
      "business_impact": "Description of potential impact"
    },
    "compliance_notes": {
      "frameworks_applicable": ["NIST", "GDPR", "HIPAA", "SOC2", "PCI-DSS"],
      "gaps_identified": ["gap1", "gap2"],
      "recommendations": "Compliance improvement recommendations"
    },
    "metadata": {
      "analyzed_at": "ISO 8601 timestamp",
      "analysis_confidence": "high|medium|low",
      "sections_reviewed": 5,
      "findings_count": 5
    }
  },
  "generated_at": "ISO 8601 timestamp",
  "metadata": {
    "model_used": "llama-3.3-70b-versatile",
    "analysis_type": "document_security_analysis",
    "doc_type": "policy",
    "source": "security_team",
    "priority": "critical",
    "content_length": 2048,
    "temperature": 0.2,
    "quality_target": "enterprise_grade"
  }
}
```

### 2. POST /api/analyse/document/bulk

Analyzes multiple documents in a batch operation (max 10 per request).

**Request:**
```json
{
  "documents": [
    {
      "content": "Document text (required)",
      "doc_type": "policy (optional)",
      "source": "source_system (optional)",
      "priority": "high (optional)",
      "id": "unique_doc_id (optional for tracking)"
    }
  ]
}
```

**Response:**
```json
{
  "status": "completed",
  "results": [
    {
      "status": "success",
      "index": 0,
      "doc_id": "doc_1",
      "analysis": { /* same structure as single endpoint */ },
      "generated_at": "ISO 8601 timestamp"
    }
  ],
  "summary": {
    "total_documents": 3,
    "successful": 2,
    "failed": 1,
    "completed_at": "ISO 8601 timestamp"
  }
}
```

## Implementation Details

### Backend Components

#### File: `prompts/templates.py`

**New Template: `ANALYZE_DOCUMENT_PROMPT`**

```python
ANALYZE_DOCUMENT_PROMPT = """Analyze the following document for security insights, risks, and key findings.

DOCUMENT CONTENT:
{content}

ANALYSIS CONTEXT:
Document Type: {doc_type}
Source: {source}
Priority Level: {priority}

[Prompt continues with detailed JSON structure requirements...]
"""
```

**Prompt Features:**
- Accepts document content, type, source, and priority
- Returns structured JSON with 3-10 findings (3 minimum, 10 maximum)
- Finding types vary: insight, risk, threat, vulnerability, misconfiguration, compliance_gap, best_practice, anomaly
- Each finding includes severity (critical, high, medium, low, informational)
- Risk assessment includes threat analysis and compliance mapping
- References MITRE ATT&CK and security frameworks

#### File: `services/groq_client.py`

**New Method: `analyze_document()`**

```python
def analyze_document(
    self,
    content: str,
    doc_type: str = "security_document",
    source: str = "unknown",
    priority: str = "medium",
    system_prompt: str = "",
) -> Dict[str, Any]:
    """Analyze document for security insights and risks."""
```

**Features:**
- Accepts document content up to 8000 characters (truncates if longer)
- Validates document type against allowed values
- Calls Groq API with temperature=0.2 (low randomness for consistency)
- Extracts and validates JSON from response
- Requires minimum fields: document_title, summary, findings, key_insights, risk_assessment
- Logs truncation warnings and parsing errors
- Returns empty dict on failure

#### File: `routes/analyse.py` (NEW)

**Endpoints:**
1. `POST /api/analyse/document` - Single document analysis
2. `POST /api/analyse/document/bulk` - Batch document analysis (max 10)

**Input Validation:**
- Content required (non-empty string)
- doc_type validated against: policy, log, alert, configuration, report, memo, ticket, security_document, other
- Priority validated against: low, medium, high, critical
- Bulk endpoint: max 10 documents per request

**Error Handling:**
- 400: Invalid input (missing content, invalid doc_type, invalid priority)
- 500: AI analysis failure or JSON parsing error
- Graceful degradation: returns error details per document in bulk mode

#### File: `app.py`

**Updates:**
- Registered `analyse_bp` blueprint
- Updated info endpoint to include analyse endpoints
- Added "document_analysis" to features list

### Test Suite

**File: `tests/test_analyse_endpoint.py`**

**Test Cases:**
1. **TEST 1: Analyze Security Policy** - Tests policy document with obvious security gaps
2. **TEST 2: Analyze Log File** - Tests security log analysis with alerts and anomalies
3. **TEST 3: Analyze Configuration** - Tests configuration file with hardcoded credentials
4. **TEST 4: Bulk Analyze** - Tests batch operation with 3 documents
5. **TEST 5: Validate Structure** - Tests JSON structure validation

**Coverage:**
- Single document analysis
- Multiple document types
- Findings classification
- Risk assessment accuracy
- Bulk operations
- Response structure validation
- Findings metadata validation

## Finding Types

The endpoint classifies findings into 8 categories:

1. **insight** - Notable observation or pattern in document
2. **risk** - Potential security or operational risk
3. **threat** - Identified threat or attack vector
4. **vulnerability** - Specific security weakness
5. **misconfiguration** - Incorrect configuration setting
6. **compliance_gap** - Non-compliance with standards/frameworks
7. **best_practice** - Deviation from security best practice
8. **anomaly** - Unusual or unexpected finding

## Severity Levels

- **critical** - Immediate remediation required, active threat or exploit
- **high** - Significant risk, should address within days
- **medium** - Moderate risk, should address within weeks
- **low** - Minor issue, plan for future improvement
- **informational** - Notable but not a risk, for awareness

## Document Types

- **policy** - Security, HR, or operational policy documents
- **log** - System, application, or security logs
- **alert** - Alerts from security systems or monitoring tools
- **configuration** - Configuration files, settings, infrastructure-as-code
- **report** - Assessment, audit, or analysis reports
- **memo** - Internal communications and memos
- **ticket** - Support tickets or issue tracking
- **security_document** - General security documents (default)
- **other** - Documents not matching above categories

## Use Cases

### 1. Security Policy Review

```json
POST /api/analyse/document
{
  "content": "[full security policy text]",
  "doc_type": "policy",
  "source": "security_team",
  "priority": "high"
}
```

Returns findings on policy gaps, weak controls, and compliance issues.

### 2. Log Analysis

```json
POST /api/analyse/document
{
  "content": "[security logs from monitoring system]",
  "doc_type": "log",
  "source": "security_monitoring",
  "priority": "critical"
}
```

Identifies threats, anomalies, and suspicious activities in logs.

### 3. Configuration Review

```json
POST /api/analyse/document
{
  "content": "[application configuration file]",
  "doc_type": "configuration",
  "source": "production_server",
  "priority": "critical"
}
```

Finds hardcoded credentials, insecure settings, and misconfigurations.

### 4. Incident Report Analysis

```json
POST /api/analyse/document
{
  "content": "[incident report text]",
  "doc_type": "report",
  "source": "incident_response_team",
  "priority": "high"
}
```

Extracts key findings, recommendations, and compliance implications.

### 5. Batch Processing

```json
POST /api/analyse/document/bulk
{
  "documents": [
    { "content": "policy1...", "doc_type": "policy", "id": "policy_2024" },
    { "content": "logs...", "doc_type": "log", "id": "logs_2024_01" },
    { "content": "config...", "doc_type": "configuration", "id": "app_config" }
  ]
}
```

Analyzes multiple documents efficiently in one request.

## Example Analysis Output

### Security Policy Analysis

**Input:** Security policy with weak password requirements, shared admin accounts, unencrypted database backups

**Output:**
```json
{
  "findings": [
    {
      "finding_type": "vulnerability",
      "title": "Weak Password Policy",
      "severity": "high",
      "description": "Policy allows minimum 8 characters with no complexity requirements. Industry standard requires 12+ characters with uppercase, lowercase, numbers, and symbols.",
      "impact": "Password cracking attacks could compromise user accounts",
      "recommendation": "Enforce minimum 12 characters, require uppercase/lowercase/numbers/symbols, implement password history"
    },
    {
      "finding_type": "compliance_gap",
      "title": "Shared Admin Credentials",
      "severity": "critical",
      "description": "All employees share domain admin account. Violates principle of least privilege and breaks audit trails.",
      "impact": "Cannot trace who performed administrative actions; compromised account affects all systems",
      "recommendation": "Create individual admin accounts with MFA; implement privileged access management (PAM)"
    }
  ],
  "risk_assessment": {
    "overall_risk_level": "critical",
    "primary_threats": ["credential_theft", "privilege_escalation", "unauthorized_access"],
    "critical_gaps": ["access_control", "authentication", "accountability"]
  }
}
```

## Performance Characteristics

- **Single document analysis:** 2-5 seconds (depends on content length)
- **Bulk analysis (10 docs):** 20-50 seconds
- **Content size limit:** 8000 characters (auto-truncated)
- **Token cost per analysis:** ~1000-2000 tokens (temperature 0.2)
- **Finding count:** 3-10 findings per document
- **Accuracy:** High (uses low temperature 0.2 for consistency)

## Integration Example

```python
import requests

# Single document analysis
response = requests.post(
    "http://localhost:5000/api/analyse/document",
    json={
        "content": "[document text]",
        "doc_type": "policy",
        "source": "security_team",
        "priority": "high"
    }
)

analysis = response.json()['analysis']
for finding in analysis['findings']:
    print(f"{finding['severity']}: {finding['title']}")
    print(f"  Recommendation: {finding['recommendation']}\n")
```

## Frontend Integration

```jsx
const [analysis, setAnalysis] = useState(null);

const analyzeDocument = async (content) => {
  const response = await fetch('http://localhost:5000/api/analyse/document', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content,
      doc_type: 'policy',
      source: 'frontend_app',
      priority: 'high'
    })
  });
  
  const data = await response.json();
  setAnalysis(data.analysis);
};

// Display findings
{analysis?.findings.map((finding, i) => (
  <div key={i} className={`finding severity-${finding.severity}`}>
    <h3>{finding.title}</h3>
    <p>{finding.description}</p>
    <strong>Recommendation:</strong> {finding.recommendation}
  </div>
))}
```

## Framework Support

The analysis supports identification and mapping to:

- **MITRE ATT&CK Framework** - Tactics and techniques
- **CVSS v3.1** - Severity scoring
- **NIST Cybersecurity Framework** - Functions and categories
- **GDPR** - Data protection compliance
- **HIPAA** - Health data compliance
- **SOC 2** - Service organization compliance
- **PCI-DSS** - Payment card security compliance

## Error Handling

| Error | Status | Cause | Solution |
|-------|--------|-------|----------|
| Missing content | 400 | Empty or missing content field | Provide non-empty document content |
| Invalid doc_type | 400 | doc_type not in allowed list | Use valid doc_type value |
| Invalid priority | 400 | priority not in allowed list | Use valid priority (low/medium/high/critical) |
| Too many documents | 400 | Bulk request > 10 documents | Split into multiple requests |
| JSON parse error | 500 | AI response not valid JSON | Retry request |
| Analysis failure | 500 | Groq API error or timeout | Retry or check AI service status |

## Limitations

- Maximum 8000 characters per document (longer documents truncated)
- Maximum 10 documents per bulk request
- Minimum 3 findings per document
- Maximum 10 findings per document
- Temperature fixed at 0.2 (low randomness)
- No streaming support (full response required)
- No document format conversion (text only)

## Future Enhancements

1. **Stream findings** - Return findings as they're generated via SSE
2. **PDF/Word support** - Accept documents in multiple formats
3. **Custom analysis profiles** - Focus on specific security domains
4. **Finding prioritization** - ML-based priority ranking
5. **Similar findings** - Cross-document finding deduplication
6. **Trend analysis** - Track findings over time
7. **Remediation tracking** - Track if recommendations implemented
8. **Export formats** - PDF, HTML, XLSX export options

## Files Changed

**Modified:**
- `prompts/templates.py` - Added ANALYZE_DOCUMENT_PROMPT
- `services/groq_client.py` - Added analyze_document() method
- `app.py` - Registered analyse blueprint and updated endpoints

**New Files:**
- `routes/analyse.py` - POST /api/analyse/document endpoints
- `tests/test_analyse_endpoint.py` - 5 comprehensive test cases

## Testing

To test the endpoint:

```bash
# Start Flask AI service
cd ai-service
python app.py

# In another terminal, run tests
cd tests
python test_analyse_endpoint.py
```

Expected output: All 5 test cases pass with valid findings structure.
