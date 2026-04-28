"""Recommend endpoint for incident response actions and remediation."""

from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from prompts.templates import SYSTEM_PROMPT, RECOMMEND_ACTIONS_PROMPT
from utils import require_json, handle_errors, validate_required_fields
import logging
from datetime import datetime, timezone


logger = logging.getLogger(__name__)
recommend_bp = Blueprint("recommend", __name__, url_prefix="/api/recommend")


def get_groq_client():
    """Get Groq client instance."""
    try:
        return GroqClient()
    except ValueError as e:
        raise ValueError(f"Groq client initialization failed: {str(e)}")


@recommend_bp.route("", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["incident_type", "severity", "description"])
def recommend_actions():
    """Generate 3 actionable recommendations for an incident as JSON array.
    
    Request body:
    {
        "incident_type": "ransomware|data_exfiltration|insider_threat|sql_injection|phishing|apt|ddos|malware|other",
        "severity": "critical|high|medium|low",
        "description": "Incident description"
    }
    
    Returns:
    {
        "status": "success",
        "incident_type": "ransomware",
        "severity": "critical",
        "recommendations": [
            {
                "action_type": "isolate_systems",
                "description": "Immediately disconnect affected systems...",
                "priority": 1
            },
            {
                "action_type": "reset_credentials",
                "description": "Reset all domain admin credentials...",
                "priority": 1
            },
            {
                "action_type": "enable_mfa",
                "description": "Enable MFA on critical systems...",
                "priority": 2
            }
        ],
        "generated_at": "ISO 8601 timestamp",
        "metadata": {
            "model_used": "llama-3.3-70b-versatile",
            "response_type": "structured_action_recommendations",
            "recommendation_count": 3,
            "framework": "NIST Incident Response"
        }
    }
    """
    data = request.get_json()
    
    # Validate and extract input
    incident_type = data.get("incident_type", "").strip().lower()
    severity = data.get("severity", "").strip().lower()
    description = data.get("description", "").strip()
    
    # Validate required fields
    if not incident_type:
        raise ValueError("Incident type is required")
    if not severity:
        raise ValueError("Severity level is required")
    if not description:
        raise ValueError("Description cannot be empty")
    
    # Validate incident type
    valid_types = ["ransomware", "data_exfiltration", "insider_threat", "sql_injection", "phishing", "apt", "ddos", "malware", "other"]
    if incident_type not in valid_types:
        raise ValueError(f"Invalid incident type. Must be one of: {', '.join(valid_types)}")
    
    # Validate severity
    valid_severities = ["critical", "high", "medium", "low"]
    if severity not in valid_severities:
        raise ValueError(f"Invalid severity. Must be one of: {', '.join(valid_severities)}")
    
    # Generate timestamp
    generated_at = datetime.now(timezone.utc).isoformat()
    
    # Call Groq for structured recommendations
    client = get_groq_client()
    recommendations = client.recommend_structured(
        incident_type=incident_type,
        severity=severity,
        description=description,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Validate we got recommendations
    if not recommendations:
        raise ValueError("Failed to generate recommendations from AI model")
    
    # Return structured response
    return jsonify({
        "status": "success",
        "incident_type": incident_type,
        "severity": severity,
        "recommendations": recommendations,
        "generated_at": generated_at,
        "metadata": {
            "model_used": client.model,
            "response_type": "structured_action_recommendations",
            "recommendation_count": len(recommendations),
            "framework": "NIST Incident Response",
            "temperature": 0.2,
            "quality_target": "actionable_enterprise_grade"
        }
    }), 200


@recommend_bp.route("/escalation", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["incident_type", "severity"])
def escalation_procedure():
    """Generate escalation procedures and notification plan.
    
    Request body:
    {
        "incident_type": "ransomware|...",
        "severity": "critical|high|medium|low",
        "description": "Brief incident description (optional)"
    }
    
    Returns escalation contacts, notification procedures, and compliance requirements
    """
    data = request.get_json()
    
    incident_type = data.get("incident_type", "").strip().lower()
    severity = data.get("severity", "").strip().lower()
    description = data.get("description", "").strip()
    
    generated_at = datetime.now(timezone.utc).isoformat()
    
    client = get_groq_client()
    
    # Create escalation prompt
    escalation_prompt = f"""Based on a {severity} severity {incident_type} incident:

Incident Details: {description if description else 'Not provided'}

Please provide:
1. Immediate escalation contacts and chain of command
2. Notification procedures and timelines
3. Regulatory/compliance notification requirements
4. Customer communication strategy
5. External party notifications (law enforcement, etc.)
6. Documentation and evidence preservation requirements

Organize by priority and timeline."""
    
    response = client.chat(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": escalation_prompt}
        ]
    )
    
    return jsonify({
        "status": "success",
        "incident_type": incident_type,
        "severity": severity,
        "escalation_procedures": response,
        "generated_at": generated_at,
        "metadata": {
            "model_used": client.model,
            "response_type": "escalation_procedures",
            "includes": ["notification_plan", "compliance_requirements", "communication_strategy"]
        }
    }), 200


@recommend_bp.route("/remediation", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["incident_type", "root_cause"])
def remediation_plan():
    """Generate comprehensive remediation and prevention plan.
    
    Request body:
    {
        "incident_type": "ransomware|...",
        "root_cause": "Description of root cause",
        "affected_systems": "List of affected systems (optional)",
        "current_controls": "Existing security controls (optional)"
    }
    
    Returns detailed remediation steps, preventive measures, and long-term improvements
    """
    data = request.get_json()
    
    incident_type = data.get("incident_type", "").strip().lower()
    root_cause = data.get("root_cause", "").strip()
    affected_systems = data.get("affected_systems", "").strip()
    current_controls = data.get("current_controls", "").strip()
    
    if not root_cause:
        raise ValueError("Root cause description is required")
    
    generated_at = datetime.now(timezone.utc).isoformat()
    
    client = get_groq_client()
    
    # Create remediation prompt
    remediation_prompt = f"""Based on a {incident_type} incident with the following details:

Root Cause: {root_cause}
Affected Systems: {affected_systems if affected_systems else 'Not specified'}
Current Controls: {current_controls if current_controls else 'Not specified'}

Please provide:
1. Immediate remediation steps (24-48 hours)
2. Short-term fixes (1-2 weeks)
3. Medium-term hardening (1-4 weeks)
4. Long-term improvements (ongoing)
5. Preventive measures to avoid recurrence
6. Security control recommendations
7. Process improvements and policy updates
8. Timeline and resource requirements

Prioritize by impact and feasibility."""
    
    response = client.chat(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": remediation_prompt}
        ]
    )
    
    return jsonify({
        "status": "success",
        "incident_type": incident_type,
        "remediation_plan": response,
        "generated_at": generated_at,
        "metadata": {
            "model_used": client.model,
            "response_type": "remediation_plan",
            "timeline_phases": ["immediate", "short_term", "medium_term", "long_term"],
            "includes": ["preventive_measures", "control_recommendations", "process_improvements"]
        }
    }), 200
