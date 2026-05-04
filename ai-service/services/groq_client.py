"""
Groq API client for incident response analysis.
Handles AI-powered incident analysis using Groq's mixtral-8x7b-versatile model.
Includes Redis caching for performance optimization.
"""

import os
import logging
import hashlib
import json
from groq import Groq
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


def _get_cache():
    """Get Redis cache instance from app context."""
    try:
        from app import get_redis_cache
        return get_redis_cache()
    except ImportError:
        return None


def _cache_key(prefix: str, *args) -> str:
    """Generate cache key from prefix and arguments."""
    key_str = f"{prefix}:" + ":".join(str(arg) for arg in args)
    return f"groq:{hashlib.md5(key_str.encode()).hexdigest()}"


class GroqClient:
    """Client for Groq API incident analysis."""

    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        """Initialize Groq client.
        
        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
            model: Model to use (default: mixtral-8x7b-32768)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.client = Groq()
        self.model = model
        logger.info(f"Initialized Groq client with model: {model}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        top_p: float = 1.0,
        use_cache: bool = True,
    ) -> str:
        """Low-level chat completion API wrapper with Redis caching.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Override model (uses self.model if not provided)
            temperature: Sampling temperature (0.3 for consistency)
            max_tokens: Maximum response tokens (2048 for comprehensive output)
            top_p: Nucleus sampling parameter
            use_cache: Whether to use Redis cache (default True)
            
        Returns:
            Response text from the model
        """
        try:
            model = model or self.model
            
            # Generate cache key from messages
            if use_cache:
                cache_key = _cache_key(
                    "chat",
                    model,
                    temperature,
                    max_tokens,
                    json.dumps(messages, sort_keys=True)
                )
                cache = _get_cache()
                
                # Try to get from cache
                if cache:
                    cached_response = cache.get(cache_key)
                    if cached_response:
                        logger.debug(f"Cache hit for key: {cache_key}")
                        return cached_response
            
            # Call Groq API
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
            )
            result = response.choices[0].message.content
            
            # Cache the response (30 minute TTL)
            if use_cache and cache:
                try:
                    cache.setex(cache_key, 1800, result)
                    logger.debug(f"Cached response with key: {cache_key}")
                except Exception as e:
                    logger.debug(f"Failed to cache response: {str(e)}")
            
            return result
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            raise

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        top_p: float = 1.0,
    ):
        """Streaming chat completion API wrapper using Server-Sent Events.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Override model (uses self.model if not provided)
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
            top_p: Nucleus sampling parameter
            
        Yields:
            Token strings as they arrive from the API
        """
        try:
            model = model or self.model
            stream = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error calling Groq streaming API: {str(e)}")
            raise

    def analyze_incident(
        self,
        incident_description: str,
        context: str = "",
        system_prompt: str = "",
        title: str = "Security Incident",
    ) -> str:
        """Analyze a security incident using the prompt template.
        
        Args:
            incident_description: Detailed incident description
            context: Additional context about the incident
            system_prompt: System prompt defining analyst persona
            title: Incident title
            
        Returns:
            Comprehensive incident analysis
        """
        from prompts.templates import ANALYZE_INCIDENT_USER_PROMPT

        # Format the user prompt template
        user_prompt = ANALYZE_INCIDENT_USER_PROMPT.format(
            title=title,
            description=incident_description,
            context=context or "No additional context provided.",
            severity_hint="To be determined based on analysis"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        logger.info(f"Analyzing incident: {title}")
        return self.chat(messages)

    def recommend_actions(
        self,
        incident_type: str,
        severity: str,
        description: str,
        system_prompt: str = "",
    ) -> str:
        """Generate action recommendations for an incident.
        
        Args:
            incident_type: Type of incident (ransomware, APT, etc.)
            severity: Severity level (critical, high, medium, low)
            description: Incident description
            system_prompt: System prompt
            
        Returns:
            Action recommendations
        """
        from prompts.templates import RECOMMEND_ACTIONS_PROMPT

        user_prompt = RECOMMEND_ACTIONS_PROMPT.format(
            incident_type=incident_type,
            severity=severity,
            description=description
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        logger.info(f"Generating recommendations for {incident_type} ({severity})")
        return self.chat(messages)

    def find_similar(
        self,
        incident_summary: str,
        system_prompt: str = "",
    ) -> str:
        """Find similar incidents from knowledge base.
        
        Args:
            incident_summary: Summary of the analyzed incident
            system_prompt: System prompt
            
        Returns:
            Similar incidents and patterns
        """
        from prompts.templates import FIND_SIMILAR_USER_PROMPT

        user_prompt = FIND_SIMILAR_USER_PROMPT.format(
            incident_summary=incident_summary
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        logger.info("Finding similar incidents")
        return self.chat(messages)

    def recommend_structured(
        self,
        incident_type: str,
        severity: str,
        description: str,
        system_prompt: str = "",
    ) -> List[Dict[str, Any]]:
        """Generate 3 structured actionable recommendations as JSON array.
        
        Args:
            incident_type: Type of incident (ransomware, APT, etc.)
            severity: Severity level (critical, high, medium, low)
            description: Incident description
            system_prompt: System prompt
            
        Returns:
            List of 3 recommendation dictionaries with action_type, description, priority
        """
        import json
        from prompts.templates import STRUCTURED_RECOMMENDATIONS_PROMPT

        user_prompt = STRUCTURED_RECOMMENDATIONS_PROMPT.format(
            incident_type=incident_type,
            severity=severity,
            description=description
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        logger.info(f"Generating structured recommendations for {incident_type} ({severity})")
        
        response = self.chat(messages, temperature=0.2, max_tokens=1024)
        
        try:
            # Extract JSON from response (handle cases where Groq may add extra text)
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                recommendations = json.loads(json_str)
                
                # Validate structure
                if isinstance(recommendations, list) and len(recommendations) > 0:
                    for rec in recommendations:
                        if not all(k in rec for k in ['action_type', 'description', 'priority']):
                            logger.warning(f"Recommendation missing required fields: {rec}")
                    
                    # Ensure we have 3 recommendations
                    return recommendations[:3] if len(recommendations) >= 3 else recommendations
            
            logger.error(f"Failed to parse recommendations JSON: {response}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in recommendations: {str(e)}")
            return []

    def generate_report(
        self,
        title: str,
        incident_type: str,
        severity: str,
        description: str,
        discovery_date: str = "Unknown",
        current_status: str = "Under Investigation",
        system_prompt: str = "",
    ) -> Dict[str, Any]:
        """Generate a comprehensive incident response report in JSON format.
        
        Args:
            title: Incident title
            incident_type: Type of incident
            severity: Severity level
            description: Incident description
            discovery_date: Date incident was discovered
            current_status: Current incident status
            system_prompt: System prompt
            
        Returns:
            Dictionary with report structure (title, executive_summary, overview, top_items, recommendations)
        """
        import json
        from prompts.templates import GENERATE_REPORT_PROMPT

        user_prompt = GENERATE_REPORT_PROMPT.format(
            title=title,
            incident_type=incident_type,
            severity=severity,
            description=description,
            discovery_date=discovery_date,
            current_status=current_status
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        logger.info(f"Generating report for {incident_type} incident: {title}")
        
        response = self.chat(messages, temperature=0.2, max_tokens=2048)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                report = json.loads(json_str)
                
                # Validate structure
                required_fields = ['title', 'executive_summary', 'overview', 'top_items', 'recommendations']
                if all(k in report for k in required_fields):
                    logger.info(f"Report generated successfully with all required fields")
                    return report
                else:
                    missing = [k for k in required_fields if k not in report]
                    logger.warning(f"Report missing fields: {missing}")
                    return report if report else {}
            
            logger.error(f"Failed to parse report JSON: {response}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in report generation: {str(e)}")
            return {}

    def generate_report_stream(
        self,
        title: str,
        incident_type: str,
        severity: str,
        description: str,
        discovery_date: str = "Unknown",
        current_status: str = "Under Investigation",
        system_prompt: str = "",
    ):
        """Generate a comprehensive incident response report with streaming output.
        
        Streams tokens in real-time as they are generated by the AI model.
        
        Args:
            title: Incident title
            incident_type: Type of incident
            severity: Severity level
            description: Incident description
            discovery_date: Date incident was discovered
            current_status: Current incident status
            system_prompt: System prompt
            
        Yields:
            Token strings as they arrive from the API
        """
        from prompts.templates import GENERATE_REPORT_PROMPT

        user_prompt = GENERATE_REPORT_PROMPT.format(
            title=title,
            incident_type=incident_type,
            severity=severity,
            description=description,
            discovery_date=discovery_date,
            current_status=current_status
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        logger.info(f"Streaming report generation for {incident_type} incident: {title}")
        
        # Stream tokens from the chat completion
        for token in self.chat_stream(messages, temperature=0.2, max_tokens=2048):
            yield token

    def analyze_document(
        self,
        content: str,
        doc_type: str = "security_document",
        source: str = "unknown",
        priority: str = "medium",
        system_prompt: str = "",
    ) -> Dict[str, Any]:
        """Analyze a document for security insights, risks, and key findings.
        
        Args:
            content: Document text content to analyze
            doc_type: Type of document (policy, log, alert, configuration, report, etc.)
            source: Source of the document (system, application, team, etc.)
            priority: Priority level (low, medium, high, critical)
            system_prompt: System prompt for analyst persona
            
        Returns:
            Dictionary with analysis containing findings, insights, risks, compliance notes
        """
        import json
        from prompts.templates import ANALYZE_DOCUMENT_PROMPT

        # Truncate document if too long to avoid token limits
        max_doc_length = 8000
        if len(content) > max_doc_length:
            logger.warning(f"Document truncated from {len(content)} to {max_doc_length} characters")
            content = content[:max_doc_length]

        user_prompt = ANALYZE_DOCUMENT_PROMPT.format(
            content=content,
            doc_type=doc_type,
            source=source,
            priority=priority
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        logger.info(f"Analyzing document: {doc_type} from {source}")
        
        response = self.chat(messages, temperature=0.2, max_tokens=2048)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                analysis = json.loads(json_str)
                
                # Validate structure
                required_fields = ['document_title', 'summary', 'findings', 'key_insights', 'risk_assessment']
                if all(k in analysis for k in required_fields):
                    logger.info(f"Document analysis complete with {len(analysis.get('findings', []))} findings")
                    return analysis
                else:
                    missing = [k for k in required_fields if k not in analysis]
                    logger.warning(f"Analysis missing fields: {missing}")
                    return analysis if analysis else {}
            
            logger.error(f"Failed to parse analysis JSON: {response}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in document analysis: {str(e)}")
            return {}

    def get_embedding_model(self):
        """Get the pre-loaded sentence-transformers embedding model.
        
        Returns:
            SentenceTransformer model if available, None otherwise
        """
        try:
            from app import get_embedding_model
            model = get_embedding_model()
            if model:
                logger.debug("Using pre-loaded embedding model from app context")
                return model
        except ImportError:
            logger.debug("Could not import embedding model from app context")
            pass
        
        # Fallback: lazy load model if not pre-loaded
        try:
            logger.info("Lazy-loading sentence-transformers embedding model")
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.warning(f"Could not load embedding model: {str(e)}")
            return None

    def clear_cache(self):
        """Clear Redis cache for all Groq responses.
        
        Returns:
            Number of keys cleared
        """
        try:
            cache = _get_cache()
            if cache:
                keys = cache.keys('groq:*')
                if keys:
                    cache.delete(*keys)
                    logger.info(f"Cleared {len(keys)} cache entries")
                    return len(keys)
        except Exception as e:
            logger.warning(f"Failed to clear cache: {str(e)}")
        return 0


