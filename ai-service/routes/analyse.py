"""Document analysis endpoint for security insights and risk identification."""

from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from prompts.templates import SYSTEM_PROMPT
from utils import require_json, handle_errors, validate_required_fields
import logging
from datetime import datetime, timezone


logger = logging.getLogger(__name__)
analyse_bp = Blueprint("analyse", __name__, url_prefix="/api/analyse")


def get_groq_client():
    """Get Groq client instance."""
    try:
        return GroqClient()
    except ValueError as e:
        raise ValueError(f"Groq client initialization failed: {str(e)}")


@analyse_bp.route("/document", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["content"])
def analyse_document():
    """Analyze a document for security insights, risks, and key findings.
    
    This endpoint accepts text documents (logs, policies, alerts, configurations)
    and performs comprehensive security analysis identifying risks, vulnerabilities,
    compliance gaps, and actionable recommendations.
    
    Request body:
    {
        "content": "Full document text content (required)",
        "doc_type": "security_document|policy|log|alert|configuration|report|memo|other (optional, default: security_document)",
        "source": "Source system or team (optional, default: unknown)",
        "priority": "low|medium|high|critical (optional, default: medium)"
    }
    
    Returns:
    {
        "status": "success",
        "analysis": {
            "document_title": "Extracted or inferred title",
            "summary": "Brief overview of document",
            "findings": [
                {
                    "finding_type": "insight|risk|threat|vulnerability|misconfiguration|compliance_gap|best_practice|anomaly",
                    "title": "Finding title",
                    "description": "Detailed description",
                    "severity": "critical|high|medium|low|informational",
                    "impact": "Potential impact",
                    "recommendation": "Actionable recommendation",
                    "references": "Framework references"
                }
            ],
            "key_insights": [
                {
                    "insight": "Observable pattern or finding",
                    "significance": "Why it matters"
                }
            ],
            "risk_assessment": {
                "overall_risk_level": "critical|high|medium|low",
                "primary_threats": ["threat1", "threat2"],
                "critical_gaps": ["gap1", "gap2"],
                "immediate_actions_required": ["action1", "action2"],
                "business_impact": "Description of potential impact"
            },
            "compliance_notes": {
                "frameworks_applicable": ["NIST", "GDPR"],
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
            "doc_type": "security_document",
            "source": "unknown"
        }
    }
    """
    data = request.get_json()
    
    # Extract and validate input
    content = data.get("content", "").strip()
    if not content:
        raise ValueError("Content cannot be empty")
    
    doc_type = data.get("doc_type", "security_document").strip().lower()
    source = data.get("source", "unknown").strip()
    priority = data.get("priority", "medium").strip().lower()
    
    # Validate doc_type
    valid_doc_types = [
        "security_document", "policy", "log", "alert", "configuration",
        "report", "memo", "ticket", "other"
    ]
    if doc_type not in valid_doc_types:
        raise ValueError(f"Invalid doc_type. Must be one of: {', '.join(valid_doc_types)}")
    
    # Validate priority
    valid_priorities = ["low", "medium", "high", "critical"]
    if priority not in valid_priorities:
        raise ValueError(f"Invalid priority. Must be one of: {', '.join(valid_priorities)}")
    
    # Generate timestamp
    generated_at = datetime.now(timezone.utc).isoformat()
    
    # Call Groq to analyze document
    client = get_groq_client()
    analysis = client.analyze_document(
        content=content,
        doc_type=doc_type,
        source=source,
        priority=priority,
        system_prompt=SYSTEM_PROMPT
    )
    
    if not analysis:
        raise ValueError("Failed to analyze document")
    
    # Return structured response
    return jsonify({
        "status": "success",
        "analysis": analysis,
        "generated_at": generated_at,
        "metadata": {
            "model_used": client.model,
            "analysis_type": "document_security_analysis",
            "doc_type": doc_type,
            "source": source,
            "priority": priority,
            "content_length": len(content),
            "temperature": 0.2,
            "quality_target": "enterprise_grade"
        }
    }), 200


@analyse_bp.route("/document/bulk", methods=["POST"])
@require_json
@handle_errors
@validate_required_fields(["documents"])
def analyse_documents_bulk():
    """Analyze multiple documents in a single request (batch operation).
    
    Request body:
    {
        "documents": [
            {
                "content": "Document text (required)",
                "doc_type": "security_document (optional)",
                "source": "Source system (optional)",
                "priority": "medium (optional)",
                "id": "unique_id (optional for tracking)"
            }
        ]
    }
    
    Returns array of analysis results with same structure as /document endpoint.
    """
    data = request.get_json()
    
    documents = data.get("documents", [])
    if not documents or not isinstance(documents, list):
        raise ValueError("Documents must be a non-empty array")
    
    if len(documents) > 10:
        raise ValueError("Maximum 10 documents per batch request")
    
    results = []
    client = get_groq_client()
    
    for idx, doc in enumerate(documents):
        try:
            content = doc.get("content", "").strip()
            if not content:
                results.append({
                    "status": "error",
                    "error": "Content cannot be empty",
                    "index": idx,
                    "doc_id": doc.get("id", f"doc_{idx}")
                })
                continue
            
            doc_type = doc.get("doc_type", "security_document").strip().lower()
            source = doc.get("source", "unknown").strip()
            priority = doc.get("priority", "medium").strip().lower()
            
            analysis = client.analyze_document(
                content=content,
                doc_type=doc_type,
                source=source,
                priority=priority,
                system_prompt=SYSTEM_PROMPT
            )
            
            if analysis:
                results.append({
                    "status": "success",
                    "index": idx,
                    "doc_id": doc.get("id", f"doc_{idx}"),
                    "analysis": analysis,
                    "generated_at": datetime.now(timezone.utc).isoformat()
                })
            else:
                results.append({
                    "status": "error",
                    "error": "Failed to analyze document",
                    "index": idx,
                    "doc_id": doc.get("id", f"doc_{idx}")
                })
        
        except Exception as e:
            logger.error(f"Error analyzing document {idx}: {str(e)}")
            results.append({
                "status": "error",
                "error": str(e),
                "index": idx,
                "doc_id": doc.get("id", f"doc_{idx}")
            })
    
    success_count = sum(1 for r in results if r.get("status") == "success")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    return jsonify({
        "status": "completed",
        "results": results,
        "summary": {
            "total_documents": len(documents),
            "successful": success_count,
            "failed": error_count,
            "completed_at": datetime.now(timezone.utc).isoformat()
        }
    }), 200
