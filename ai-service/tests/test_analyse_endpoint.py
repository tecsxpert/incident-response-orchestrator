"""
Test cases for document analysis endpoint.
Tests analyze_document functionality with various document types.
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:5000"


def test_analyse_security_policy():
    """Test analyzing a security policy document."""
    print("\n" + "="*80)
    print("TEST 1: Analyze Security Policy Document")
    print("="*80)
    
    policy_content = """
    INFORMATION SECURITY POLICY
    
    1. PASSWORD REQUIREMENTS
    - Minimum 8 characters
    - Must contain uppercase and lowercase
    - Users may write passwords on sticky notes
    
    2. ACCESS CONTROL
    - All employees share domain admin account
    - Contractor accounts never expire
    - VPN requires simple PIN only
    
    3. DATA CLASSIFICATION
    - All data stored in public S3 bucket
    - Database backups uploaded to public GitHub
    - Credit card data stored in plain text
    
    4. INCIDENT RESPONSE
    - No incident response plan exists
    - IT manager handles all incidents manually
    - No logging or monitoring configured
    
    5. VENDOR MANAGEMENT
    - Vendors given full system access
    - No security assessments required
    - Software from untrusted sources installed directly
    """
    
    payload = {
        "content": policy_content,
        "doc_type": "policy",
        "source": "security_team",
        "priority": "critical"
    }
    
    response = requests.post(f"{BASE_URL}/api/analyse/document", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis Status: {data['status']}")
        print(f"Document Title: {data['analysis'].get('document_title', 'N/A')}")
        print(f"Summary: {data['analysis'].get('summary', 'N/A')[:100]}...")
        print(f"\nFindings Count: {len(data['analysis'].get('findings', []))}")
        for i, finding in enumerate(data['analysis'].get('findings', [])[:3], 1):
            print(f"\n  Finding {i}:")
            print(f"    Type: {finding.get('finding_type', 'N/A')}")
            print(f"    Title: {finding.get('title', 'N/A')}")
            print(f"    Severity: {finding.get('severity', 'N/A')}")
        
        risk = data['analysis'].get('risk_assessment', {})
        print(f"\nOverall Risk Level: {risk.get('overall_risk_level', 'N/A')}")
        print(f"Primary Threats: {', '.join(risk.get('primary_threats', [])[:3])}")
        print(f"Immediate Actions: {', '.join(risk.get('immediate_actions_required', [])[:2])}")
        
        metadata = data['analysis'].get('metadata', {})
        print(f"\nAnalysis Confidence: {metadata.get('analysis_confidence', 'N/A')}")
        print(f"Total Findings: {metadata.get('findings_count', 'N/A')}")
    else:
        print(f"Error: {response.text}")


def test_analyse_log_file():
    """Test analyzing a security log file."""
    print("\n" + "="*80)
    print("TEST 2: Analyze Security Log File")
    print("="*80)
    
    log_content = """
    2024-01-15 09:23:45 [ALERT] Failed login attempts: 250 failed attempts from IP 192.168.1.100
    2024-01-15 09:24:12 [ERROR] Database connection timeout from service account
    2024-01-15 09:25:33 [ALERT] Suspicious PowerShell execution: encoded command detected
    2024-01-15 09:26:01 [INFO] User admin logged in via RDP from 10.0.0.50
    2024-01-15 09:27:15 [ALERT] Large data transfer detected: 5GB to external IP 203.0.113.45
    2024-01-15 09:28:42 [ERROR] SSL certificate validation failed for internal service
    2024-01-15 09:29:50 [ALERT] Privilege escalation attempt: normal user tried to access admin folder
    2024-01-15 09:30:22 [INFO] Backup completed successfully
    2024-01-15 09:31:44 [ALERT] Registry modification detected on server: HKLM\\System\\RUN key
    2024-01-15 09:32:11 [ERROR] File integrity check failed for critical binaries
    """
    
    payload = {
        "content": log_content,
        "doc_type": "log",
        "source": "security_monitoring",
        "priority": "high"
    }
    
    response = requests.post(f"{BASE_URL}/api/analyse/document", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis Status: {data['status']}")
        print(f"Document Title: {data['analysis'].get('document_title', 'N/A')}")
        
        findings = data['analysis'].get('findings', [])
        print(f"Findings identified: {len(findings)}")
        
        insights = data['analysis'].get('key_insights', [])
        print(f"Key Insights: {len(insights)}")
        for i, insight in enumerate(insights[:2], 1):
            print(f"  {i}. {insight.get('insight', 'N/A')}")
        
        risk = data['analysis'].get('risk_assessment', {})
        print(f"\nOverall Risk: {risk.get('overall_risk_level', 'N/A')}")
        print(f"Critical Gaps: {risk.get('critical_gaps', [])}")
    else:
        print(f"Error: {response.text}")


def test_analyse_configuration():
    """Test analyzing a system configuration file."""
    print("\n" + "="*80)
    print("TEST 3: Analyze System Configuration")
    print("="*80)
    
    config_content = """
    [Database]
    Host: 192.168.1.50
    Port: 3306
    Username: root
    Password: password123
    SSL: false
    Timeout: 30
    
    [Application]
    DebugMode: true
    LogLevel: DEBUG
    CacheTTL: 0
    SessionTimeout: 28800
    EncryptionKey: 
    
    [Security]
    CORS: *
    AllowedOrigins: *
    EnableCSRF: false
    PasswordPolicy: none
    MFARequired: false
    
    [API]
    APIKey: sk-12345678abcdefghij
    RateLimiting: disabled
    IPWhitelist: none
    LogRequests: true
    PublicEndpoints: /api/*
    """
    
    payload = {
        "content": config_content,
        "doc_type": "configuration",
        "source": "production_server",
        "priority": "critical"
    }
    
    response = requests.post(f"{BASE_URL}/api/analyse/document", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis Status: {data['status']}")
        print(f"Document Title: {data['analysis'].get('document_title', 'N/A')}")
        
        findings = data['analysis'].get('findings', [])
        print(f"\nTotal Findings: {len(findings)}")
        
        # Count by severity
        by_severity = {}
        for finding in findings:
            severity = finding.get('severity', 'unknown')
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        print("Findings by Severity:")
        for severity, count in sorted(by_severity.items(), reverse=True):
            print(f"  {severity}: {count}")
        
        # Show critical findings
        critical = [f for f in findings if f.get('severity') == 'critical']
        print(f"\nCritical Findings ({len(critical)}):")
        for finding in critical[:3]:
            print(f"  - {finding.get('title', 'N/A')}")
            print(f"    Recommendation: {finding.get('recommendation', 'N/A')[:80]}...")
    else:
        print(f"Error: {response.text}")


def test_analyse_document_bulk():
    """Test analyzing multiple documents in bulk."""
    print("\n" + "="*80)
    print("TEST 4: Bulk Analyze Multiple Documents")
    print("="*80)
    
    documents = [
        {
            "id": "doc_1",
            "content": "User admin created with password: admin123. SSH enabled on all ports.",
            "doc_type": "alert",
            "source": "audit_log",
            "priority": "high"
        },
        {
            "id": "doc_2",
            "content": "Database backup failed. Retention policy set to 0 days. No secondary backup exists.",
            "doc_type": "report",
            "source": "backup_system",
            "priority": "critical"
        },
        {
            "id": "doc_3",
            "content": "Security patch available for OpenSSL. Current version: 1.0.1 (EOL). Zero-day vulnerability CVE-2024-00001",
            "doc_type": "ticket",
            "source": "vulnerability_scanner",
            "priority": "critical"
        }
    ]
    
    payload = {"documents": documents}
    
    response = requests.post(f"{BASE_URL}/api/analyse/document/bulk", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Batch Status: {data['status']}")
        
        summary = data['summary']
        print(f"\nBatch Summary:")
        print(f"  Total: {summary['total_documents']}")
        print(f"  Successful: {summary['successful']}")
        print(f"  Failed: {summary['failed']}")
        
        for result in data['results']:
            if result['status'] == 'success':
                print(f"\n✓ {result['doc_id']}: {result['analysis'].get('document_title', 'N/A')}")
                findings = result['analysis'].get('findings', [])
                print(f"  Findings: {len(findings)}")
            else:
                print(f"\n✗ {result['doc_id']}: {result.get('error', 'Unknown error')}")
    else:
        print(f"Error: {response.text}")


def test_validate_findings_structure():
    """Test that findings have proper structure."""
    print("\n" + "="*80)
    print("TEST 5: Validate Findings Structure")
    print("="*80)
    
    content = """
    SECURITY ASSESSMENT REPORT
    
    System: Production Web Server
    Assessment Date: 2024-01-15
    Assessor: Security Team
    
    FINDINGS:
    1. SSL/TLS: Self-signed certificate, not validated
    2. Database: No connection encryption
    3. Authentication: No multi-factor authentication
    4. Logging: Application logs stored in world-readable directory
    5. Dependencies: 45 known vulnerabilities in npm packages
    """
    
    payload = {
        "content": content,
        "doc_type": "report",
        "source": "security_audit",
        "priority": "high"
    }
    
    response = requests.post(f"{BASE_URL}/api/analyse/document", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        analysis = data['analysis']
        
        # Validate top-level structure
        required_fields = ['document_title', 'summary', 'findings', 'key_insights', 'risk_assessment', 'metadata']
        print("Validating Analysis Structure:")
        for field in required_fields:
            present = field in analysis
            print(f"  {field}: {'✓' if present else '✗'}")
        
        # Validate finding structure
        findings = analysis.get('findings', [])
        if findings:
            print(f"\nValidating First Finding Structure ({len(findings)} findings total):")
            finding = findings[0]
            required_finding_fields = ['finding_type', 'title', 'description', 'severity', 'impact', 'recommendation']
            for field in required_finding_fields:
                present = field in finding
                print(f"  {field}: {'✓' if present else '✗'}")
        
        # Validate risk assessment
        risk = analysis.get('risk_assessment', {})
        print(f"\nRisk Assessment Fields:")
        for field in ['overall_risk_level', 'primary_threats', 'critical_gaps', 'immediate_actions_required']:
            present = field in risk
            print(f"  {field}: {'✓' if present else '✗'}")
    else:
        print(f"Error: {response.text}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("DOCUMENT ANALYSIS ENDPOINT TEST SUITE")
    print("="*80)
    
    try:
        test_analyse_security_policy()
        test_analyse_log_file()
        test_analyse_configuration()
        test_validate_findings_structure()
        test_analyse_document_bulk()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED")
        print("="*80)
    except Exception as e:
        print(f"\n✗ Test Error: {str(e)}")
        import traceback
        traceback.print_exc()
