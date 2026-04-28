"""Real-world incident test cases for prompt quality validation."""

TEST_CASES = [
    {
        "name": "TEST_CASE_1: Ransomware Attack",
        "title": "Critical: Ransomware Encryption Attack on File Servers",
        "description": "On March 15, 2024 at 14:30 UTC, file servers FS-001 through FS-005 became inaccessible. Users reported all files replaced with .ENCRYPT extension. Ransom note found: Your files are encrypted. Contact ransomgang. Approximately 500GB of critical business files affected including customer data, financial records, and proprietary source code. Investigation shows lateral movement from compromised workstation WS-087 (marketing dept, user: jsmith). Initial access likely through spear-phishing email received 2 weeks prior. No backups were accessed. Network segmentation between marketing and file servers was inadequate.",
        "context": "We have limited air-gapped backups from 2 weeks ago. Critical business impact - customer deliverables delayed.",
        "severity_hint": "Critical"
    },
    {
        "name": "TEST_CASE_2: Data Exfiltration",
        "title": "High: Unauthorized Data Exfiltration from Customer Database",
        "description": "Database server DB-PROD-02 logs show unusual outbound HTTPS connections on 2024-03-12 from 09:15 to 11:47 UTC. SQL queries accessed customer PII table customers_pii containing 47283 records (names, addresses, phone, SSN). Approximately 2.3GB of compressed data transferred to IP 185.220.101.45 (Tor exit node). Initial investigation suggests compromised database service account app_service with password last changed 180 days ago. No alerts triggered despite IDS/IPS being active. Application logs show queries executing with UNION-based data extraction pattern. Similar traffic pattern detected 3 days ago for 2 hours.",
        "context": "We are subject to GDPR and HIPAA. Customer notification may be required. Service account not part of our standard access review process.",
        "severity_hint": "High"
    },
    {
        "name": "TEST_CASE_3: Insider Threat",
        "title": "High: Suspicious Data Download by Marketing Manager",
        "description": "Marketing manager Robert Chen downloaded 1.2GB of competitive analysis research to personal Google Drive on 2024-03-14. Access logs show: 847 files accessed from research/competitive_intelligence/ over 4-hour period. Chen's manager reports he recently interviewed with competitor company TechCorp Inc. Company property laptop shows file transfer activity via Chrome to personal Google account. Email shows Chen communicating with TechCorp employee about consulting opportunity starting April. IT also discovered he visited job sites 23 times in past week and accessed salary data from HR system he should not have access to.",
        "context": "Chen is valuable employee, been with company 6 years. We need to handle carefully. Unclear if he had legitimate business reason for competitive data access.",
        "severity_hint": "High"
    },
    {
        "name": "TEST_CASE_4: SQL Injection Attack",
        "title": "Critical: SQL Injection on Customer-Facing Portal",
        "description": "Web application firewall WAF logs show 2847 suspicious SQL injection attempts against customer portal login form starting 2024-03-13 at 03:22 UTC from multiple source IPs (likely botnet). Pattern: variations of OR conditions in username/password fields. 25 successful database queries detected bypassing authentication, accessing user_accounts table. Attacker accessed credential hashes for 1240 customer accounts. Portal remained accessible during attack - no blocking triggered. Initial vector: unpatched Apache Struts vulnerability CVE-2024-XXXXX. Similar attack detected 5 days ago but incorrectly classified as failed login attempts.",
        "context": "Customer portal serves 50000 active users. We are investigating which accounts were compromised. Patching was planned but delayed due to other priorities.",
        "severity_hint": "Critical"
    },
    {
        "name": "TEST_CASE_5: Email Phishing Campaign",
        "title": "Critical: Targeted Phishing Campaign with High Compromise Rate",
        "description": "Email gateway blocked 2400 phishing emails on 2024-03-16 targeting executives with subject Important Board Meeting Updates. 23 emails reached inboxes due to evasion techniques. 8 employees clicked malicious link, 6 entered credentials on fake Office365 login page. Phishing page hosted on compromised WordPress site (evilsite.ru). Session logs show 4 of the 6 credential-entering users had their Office365 accounts accessed from IP 192.0.2.XX (Russia). Email forwarding rules set for 3 executives to forward to external account attacker@protonmail.com. Compromised accounts used to send internal phishing emails to finance department. Attackers attempted wire transfer of 2 million dollars (caught by manual verification). Attack sophistication: high - used legitimate Microsoft branding, perfect grammar, specific executive names.",
        "context": "Affects C-level executives and finance team. We have email logs and wire transfer pending. Need immediate containment. Employee training on phishing is outdated (2022).",
        "severity_hint": "Critical"
    }
]

QUALITY_CRITERIA = {
    "structure": {
        "description": "Response contains all 10 required sections",
        "weight": 50,
        "sections": [
            "Threat Classification",
            "Severity Assessment",
            "Affected Assets",
            "Incident Timeline",
            "Root Cause Analysis",
            "Impact Assessment",
            "Indicators of Compromise",
            "Immediate Response Actions",
            "Risk Assessment",
            "Recommendations"
        ]
    },
    "technical_accuracy": {
        "description": "Uses correct terminology, frameworks (CVSS, MITRE), and technical concepts",
        "weight": 20
    },
    "formatting": {
        "description": "Clear markdown formatting, proper sections, readable structure",
        "weight": 15
    },
    "terminology": {
        "description": "Uses industry-standard security terminology correctly",
        "weight": 10
    },
    "actionability": {
        "description": "Recommendations are specific and implementable",
        "weight": 5
    }
}
