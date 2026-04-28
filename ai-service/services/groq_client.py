"""
Groq API client for incident response analysis.
Handles AI-powered incident analysis using Groq's mixtral-8x7b-32768 model.
"""

import os
import logging
from groq import Groq
from typing import Optional, Dict, List, Any


logger = logging.getLogger(__name__)


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
    ) -> str:
        """Low-level chat completion API wrapper.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Override model (uses self.model if not provided)
            temperature: Sampling temperature (0.3 for consistency)
            max_tokens: Maximum response tokens (2048 for comprehensive output)
            top_p: Nucleus sampling parameter
            
        Returns:
            Response text from the model
        """
        try:
            model = model or self.model
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
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
