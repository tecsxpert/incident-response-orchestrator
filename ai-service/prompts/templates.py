"""
Professional prompt templates for incident response analysis.
Used by Groq API for AI-powered incident analysis.
"""

SYSTEM_PROMPT = """You are a cybersecurity incident response analyst. Provide structured analysis with:
- MITRE ATT&CK / CVSS / NIST context
- Technical depth with actionable guidance
- Clear sections and professional language
- Business impact assessment
- Compliance considerations where relevant"""

ANALYZE_INCIDENT_USER_PROMPT = """Analyze this security incident:

DETAILS: Title: {title} | Description: {description} | Context: {context} | Severity: {severity_hint}

Provide 6-section analysis:

## 1. Threat Classification
Classify threat type (ransomware, APT, insider threat, etc.) with MITRE ATT&CK tactics.

## 2. Severity Assessment
CVSS v3.1 base score, business/security impact ratings, justification.

## 3. Root Cause Analysis
Attack vector, entry point, exploited vulnerabilities, progression.

## 4. Impact Assessment
Technical (availability/integrity/confidentiality), business, compliance, reputational impacts.

## 5. Immediate Actions (First 24-48 hours)
Containment, isolation, evidence preservation, notification procedures.

## 6. Recommendations
Short-term (1-7 days), medium-term (1-4 weeks), long-term improvements."""

FIND_SIMILAR_USER_PROMPT = """Identify 3-4 similar historical incidents:

INCIDENT: {incident_summary}

Provide: 1) Similar incidents with details 2) Common patterns/TTPs 3) Lessons learned 4) Preventive measures"""

RECOMMEND_ACTIONS_PROMPT = """Generate 3 actionable recommendations for {severity} {incident_type}:

DETAILS: {description}

RESPOND WITH ONLY VALID JSON (no extra text):
[
  {"action_type": "...", "description": "specific action (2 sentences)", "priority": 1},
  {"action_type": "...", "description": "specific action (2 sentences)", "priority": 1},
  {"action_type": "...", "description": "specific action (2 sentences)", "priority": 2}
]"""

STRUCTURED_RECOMMENDATIONS_PROMPT = """Generate 3 recommendations for {severity} {incident_type}:

{description}

RESPOND WITH ONLY this JSON (no other text):
[
  {{"action_type": "isolate_systems", "description": "Immediately disconnect affected systems to contain threat.", "priority": 1}},
  {{"action_type": "reset_credentials", "description": "Reset admin/service account credentials on affected systems.", "priority": 1}},
  {{"action_type": "enable_monitoring", "description": "Enable enhanced monitoring and logging on critical systems.", "priority": 2}}
]"""

GENERATE_REPORT_PROMPT = """Generate incident report JSON:

Title: {title} | Type: {incident_type} | Severity: {severity}
Description: {description} | Discovery: {discovery_date} | Status: {current_status}

RESPOND WITH ONLY JSON (no other text):
{{
  "title": "Professional title",
  "executive_summary": "2-3 paragraphs for executives",
  "overview": "Technical overview with attack vector and timeline",
  "top_items": [
    {{"item": "Finding 1", "description": "Details"}},
    {{"item": "Finding 2", "description": "Details"}},
    {{"item": "Finding 3", "description": "Details"}}
  ],
  "recommendations": [
    {{"action": "Immediate action", "timeframe": "0-24 hours", "priority": "P1"}},
    {{"action": "Short-term", "timeframe": "1-7 days", "priority": "P2"}},
    {{"action": "Medium-term", "timeframe": "1-4 weeks", "priority": "P3"}}
  ]
}}"""

ANALYZE_DOCUMENT_PROMPT = """Analyze document for security insights (max 8 findings):

Type: {doc_type} | Source: {source} | Priority: {priority}

CONTENT: {content}

RESPOND WITH ONLY JSON:
{{
  "document_title": "Title",
  "summary": "2-3 sentence summary",
  "findings": [
    {{
      "finding_type": "insight|risk|threat|vulnerability|misconfiguration|compliance_gap",
      "title": "Title",
      "description": "Details with implications",
      "severity": "critical|high|medium|low|informational",
      "impact": "Potential impact",
      "recommendation": "Specific action",
      "references": "MITRE ATT&CK / CVSS / Framework"
    }}
  ],
  "key_insights": [
    {{"insight": "Observation", "significance": "Why it matters"}}
  ],
  "risk_assessment": {{
    "overall_risk_level": "critical|high|medium|low",
    "primary_threats": ["threat1", "threat2"],
    "critical_gaps": ["gap1"],
    "immediate_actions_required": ["action1"],
    "business_impact": "Impact description"
  }},
  "compliance_notes": {{
    "frameworks_applicable": ["NIST", "GDPR", "SOC2"],
    "gaps_identified": ["gap1"],
    "recommendations": "Compliance recommendations"
  }},
  "metadata": {{
    "analyzed_at": "ISO timestamp",
    "analysis_confidence": "high|medium|low",
    "sections_reviewed": 0,
    "findings_count": 0
  }}
}}"""
