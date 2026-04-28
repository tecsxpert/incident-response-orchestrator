"""Describe endpoint for incident analysis."""

from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from prompts.templates import SYSTEM_PROMPT
from utils import require_json, handle_errors, validate_required_fields
import logging


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
    """Analyze a security incident.
    
    Request body:
    {
        "title": "Incident Title",
        "description": "Detailed incident description",
        "context": "Additional context (optional)",
        "severity_hint": "Severity level (optional)"
    }
    """
    data = request.get_json()
    title = data.get("title", "Security Incident")
    description = data.get("description", "")
    context = data.get("context", "")
    severity_hint = data.get("severity_hint", "")

    client = get_groq_client()
    analysis = client.analyze_incident(
        incident_description=description,
        context=context,
        system_prompt=SYSTEM_PROMPT,
        title=title
    )

    return jsonify({
        "status": "success",
        "title": title,
        "analysis": analysis,
        "metadata": {
            "model_used": client.model,
            "analysis_type": "comprehensive_incident_assessment"
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
