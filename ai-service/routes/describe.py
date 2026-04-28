"""Describe endpoint for incident analysis."""

from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from prompts.templates import SYSTEM_PROMPT
from utils import require_json, handle_errors, validate_required_fields
import logging
from datetime import datetime, timezone


logger = logging.getLogger(__name__)
describe_bp = Blueprint("describe", __name__, url_prefix="/api/describe")


def get_groq_client():
    """Get Groq client instance."""
    try:
        return GroqClient()
    except ValueError as e:
        raise ValueError(f"Groq client initialization failed: {str(e)}")


@describe_bp.route("", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["description"])
def describe_incident():
    """Analyze a security incident with professional assessment.
    
    Request body:
    {
        "title": "Incident Title (optional)",
        "description": "Detailed incident description (required)",
        "context": "Additional context (optional)",
        "severity_hint": "Severity level (optional)"
    }
    
    Returns:
    {
        "status": "success",
        "title": "Incident title",
        "analysis": "10-section comprehensive analysis",
        "generated_at": "ISO 8601 timestamp",
        "metadata": {
            "model_used": "llama-3.3-70b-versatile",
            "analysis_type": "comprehensive_incident_assessment",
            "framework": "MITRE ATT&CK / CVSS / NIST"
        }
    }
    """
    data = request.get_json()
    
    # Validate and extract input
    description = data.get("description", "").strip()
    if not description:
        raise ValueError("Description cannot be empty")
    
    title = data.get("title", "Security Incident").strip()
    context = data.get("context", "").strip()
    severity_hint = data.get("severity_hint", "").strip()

    # Generate timestamp for when analysis was requested
    generated_at = datetime.now(timezone.utc).isoformat()

    # Load prompt template and call Groq
    client = get_groq_client()
    analysis = client.analyze_incident(
        incident_description=description,
        context=context,
        system_prompt=SYSTEM_PROMPT,
        title=title
    )

    # Return structured JSON response
    return jsonify({
        "status": "success",
        "title": title,
        "analysis": analysis,
        "generated_at": generated_at,
        "metadata": {
            "model_used": client.model,
            "analysis_type": "comprehensive_incident_assessment",
            "framework": "MITRE ATT&CK / CVSS / NIST CSF",
            "sections": 10,
            "temperature": 0.3,
            "quality_target": "professional_enterprise_grade"
        }
    }), 200


@describe_bp.route("/similar", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["incident_summary"])
def find_similar_incidents():
    """Find similar incidents."""
    data = request.get_json()
    incident_summary = data.get("incident_summary", "")

    client = get_groq_client()
    similar = client.find_similar(
        incident_summary=incident_summary,
        system_prompt=SYSTEM_PROMPT
    )

    return jsonify({
        "status": "success",
        "similar_incidents": similar
    }), 200


@describe_bp.route("/summary", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["analysis"])
def summarize_incident():
    """Generate executive summary."""
    data = request.get_json()
    analysis = data.get("analysis", "")
    max_chars = data.get("max_chars", 500)

    # Simple summarization - take first max_chars characters
    summary = analysis[:max_chars] + "..." if len(analysis) > max_chars else analysis

    return jsonify({
        "status": "success",
        "summary": summary,
        "length": len(summary)
    }), 200
