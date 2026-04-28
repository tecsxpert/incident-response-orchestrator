"""
Professional prompt templates for incident response analysis.
Used by Groq API for AI-powered incident analysis.
"""

SYSTEM_PROMPT = """You are an elite cybersecurity incident response analyst with 15+ years of experience. 
Your expertise spans threat intelligence, forensics, incident classification, and compliance frameworks.

CORE COMPETENCIES:
- MITRE ATT&CK Framework knowledge
- CVSS scoring methodology
- NIST Cybersecurity Framework
- Incident timeline reconstruction
- Root cause analysis
- Compliance requirements (GDPR, HIPAA, SOC 2, PCI-DSS)
- Multi-stage attack patterns
- Lateral movement detection
- Data exfiltration assessment

ANALYSIS PRINCIPLES:
1. Always maintain professional, technical language
2. Provide actionable recommendations
3. Consider business impact alongside technical severity
4. Identify patterns and potential lateral movement
5. Assess both immediate and long-term risks
6. Reference specific frameworks and standards
7. Prioritize containment and recovery steps
8. Include indicators of compromise when relevant
9. Consider compliance and legal implications
10. Balance technical accuracy with accessibility

RESPONSE FORMAT:
Provide structured analysis with clear sections, technical depth, and actionable guidance.
Use markdown formatting for clarity. Be comprehensive but concise."""

ANALYZE_INCIDENT_USER_PROMPT = """Analyze the following security incident comprehensively:

INCIDENT DETAILS:
Title: {title}
Description: {description}
Context: {context}
Severity Hint: {severity_hint}

Please provide a thorough incident analysis following this exact 10-section format:

## 1. Threat Classification
- Classify the threat type (e.g., ransomware, APT, insider threat, supply chain attack)
- Identify sub-category and attack methodology
- Assess confidence level in classification
- Reference MITRE ATT&CK tactics and techniques

## 2. Severity Assessment
- Calculate CVSS v3.1 base score and provide detailed rationale
- Rate business impact (Critical/High/Medium/Low)
- Rate security impact (Critical/High/Medium/Low)
- Provide justification for severity ratings
- Consider data sensitivity and system criticality

## 3. Affected Assets
- List systems, applications, and infrastructure impacted
- Identify data types and sensitivity levels
- Estimate number of users or entities affected
- Detail dependencies and potential cascading impacts
- Include geographic or organizational scope

## 4. Incident Timeline
- Document discovery date and time (if known)
- Establish likely incident start date
- Identify key events chronologically
- Estimate incident duration
- Note current status (ongoing, contained, resolved)

## 5. Root Cause Analysis
- Identify attack vector and entry point
- Detail exploited vulnerabilities or weaknesses
- Explain attack progression and lateral movement
- Assess contributing factors
- Consider supply chain or configuration issues

## 6. Impact Assessment
- Technical Impact: system availability, data integrity, confidentiality loss
- Business Impact: revenue loss, operational disruption, customer impact
- Compliance Impact: regulatory violations, reporting obligations
- Reputational Impact: brand damage, customer trust
- Quantify impact where possible

## 7. Indicators of Compromise (IoCs)
- Suspicious IP addresses or domains
- File hashes (MD5, SHA-1, SHA-256)
- File paths or registry keys
- Process names and command lines
- Network signatures or behavioral patterns
- Email addresses or usernames used in attack

## 8. Immediate Response Actions
- Prioritize containment steps (1st 24-48 hours)
- Isolation and quarantine procedures
- Evidence preservation requirements
- Notification procedures (internal, external, law enforcement)
- Emergency communication plan
- Stakeholder notification sequence

## 9. Risk Assessment
- Evaluate escalation potential
- Assess containment difficulty
- Identify critical next steps
- Consider worst-case scenarios
- Evaluate likelihood of recurrence
- Assess attacker persistence indicators

## 10. Recommendations
Short-term (24-48 hours):
- Immediate containment and isolation
- Evidence collection and preservation
- Stakeholder notification
- External reporting requirements

Medium-term (1-2 weeks):
- Deep forensic analysis
- Root cause remediation
- Security control enhancements
- System hardening
- Access review and updates

Long-term (ongoing):
- Advanced threat detection implementation
- Threat hunting for similar indicators
- Process and policy improvements
- Security awareness training
- Regular security assessments
- Backup and disaster recovery improvements

QUALITY REQUIREMENTS:
- Use professional, technical language
- Provide specific, actionable recommendations
- Reference relevant frameworks and standards
- Consider business context and priorities
- Include risk quantification where possible
- Maintain objectivity and accuracy
- Structure response clearly for readability
- Support conclusions with technical reasoning"""

FIND_SIMILAR_USER_PROMPT = """Based on the incident you analyzed, identify similar incidents from your knowledge base.

INCIDENT SUMMARY:
{incident_summary}

Please provide:
1. Similar historical incidents (3-5 examples)
2. Common patterns and TTPs
3. Attack progression patterns
4. Similar threat actors or groups
5. Lessons learned from similar incidents
6. Preventive measures that worked
7. Common mistakes and how to avoid them"""

RECOMMEND_ACTIONS_PROMPT = """Based on the incident analysis, provide detailed action recommendations:

INCIDENT TYPE: {incident_type}
SEVERITY: {severity}
DESCRIPTION: {description}

Provide structured recommendations for:
1. Immediate containment (0-24 hours)
2. Short-term remediation (1-7 days)
3. Medium-term hardening (1-4 weeks)
4. Long-term improvements (ongoing)

Include specific tools, procedures, and timeline for implementation."""

STRUCTURED_RECOMMENDATIONS_PROMPT = """Generate exactly 3 actionable recommendations for this {severity} {incident_type} incident.

INCIDENT DETAILS:
{description}

You MUST respond with ONLY a valid JSON array, no other text. Each recommendation must have exactly these fields:
- action_type: Type of action (e.g., "isolate_systems", "reset_credentials", "patch_vulnerability", "block_ips", "enable_mfa", "segment_network", "update_firewall", "increase_monitoring", "notify_authorities", "review_logs")
- description: Detailed, actionable description (2-3 sentences, specific and technical)
- priority: Priority level as integer 1-3 where 1 is highest priority

REQUIREMENTS:
- Return EXACTLY 3 recommendations
- Prioritize based on incident severity and containment needs
- Recommendations must be specific and immediately actionable
- Order by priority (highest first)
- No explanations, just the JSON array
- Each description must be specific to {incident_type} incidents
- Format: [{{...}}, {{...}}, {{...}}]

Example format:
[
  {{"action_type": "isolate_systems", "description": "Immediately disconnect affected file servers from network to prevent ransomware propagation to backup systems.", "priority": 1}},
  {{"action_type": "reset_credentials", "description": "Reset all domain admin and service account passwords, focusing on accounts with access to affected systems.", "priority": 1}},
  {{"action_type": "enable_mfa", "description": "Enable MFA on all critical systems and remote access points to prevent lateral movement using compromised credentials.", "priority": 2}}
]"""
