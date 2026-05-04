"""
Comprehensive QA Testing - All 6 Endpoints with Professional Demo Data
Tests incident analysis, recommendations, document analysis, and batch processing
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

# ANSI color codes for output
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(title):
    """Print formatted section header."""
    print(f"\n{BOLD}{BLUE}{'='*80}")
    print(f"{title}")
    print(f"{'='*80}{RESET}\n")


def print_test_result(endpoint, status_code, success):
    """Print test result."""
    result_text = f"{GREEN}✓ PASS{RESET}" if success else f"{RED}✗ FAIL{RESET}"
    print(f"{endpoint:<40} {status_code:<10} {result_text}")


def test_endpoint_1_describe():
    """Test 1: POST /api/describe - Incident Analysis"""
    print_header("ENDPOINT 1: POST /api/describe - Comprehensive Incident Analysis")
    
    demo_data = {
        "title": "Critical Ransomware Attack - Finance Department",
        "description": "On May 4, 2026 at 14:30 UTC, multiple user workstations in the Finance Department were infected with LockBit 3.0 ransomware. The attack encrypted approximately 850GB of financial records, backup databases, and critical business documentation. The threat actor has demanded $500,000 in cryptocurrency for decryption keys. Initial analysis suggests the infection originated from a phishing email containing a weaponized Excel macro that was opened by a finance analyst. The attack has propagated across the file server network and backup systems.",
        "context": "Finance department operates 45 workstations on a segmented network. Backup systems are not air-gapped. Critical infrastructure includes SAP ERP system and Oracle database servers. No recent security audits have been performed.",
        "severity_hint": "critical"
    }
    
    print(f"{YELLOW}Demo Data:{RESET}")
    print(f"Title: {demo_data['title']}")
    print(f"Severity: {demo_data['severity_hint']}")
    print(f"Description length: {len(demo_data['description'])} chars\n")
    
    try:
        response = requests.post(f"{BASE_URL}/describe", json=demo_data, timeout=30)
        success = response.status_code == 200
        
        print_test_result("POST /api/describe", response.status_code, success)
        
        if success:
            data = response.json()
            print(f"\n{YELLOW}Response Structure:{RESET}")
            print(f"  • status: {data.get('status')}")
            print(f"  • title: {data.get('title')[:60]}...")
            print(f"  • analysis length: {len(data.get('analysis', ''))} chars")
            print(f"  • generated_at: {data.get('generated_at')}")
            print(f"  • metadata.model_used: {data.get('metadata', {}).get('model_used')}")
            
            print(f"\n{YELLOW}Analysis Preview:{RESET}")
            analysis_preview = data.get('analysis', '')[:400]
            print(f"{analysis_preview}...\n")
            
            return True
        else:
            print(f"{RED}Error: {response.text}{RESET}\n")
            return False
    except Exception as e:
        print(f"{RED}Exception: {str(e)}{RESET}\n")
        return False


def test_endpoint_2_stream():
    """Test 2: POST /api/describe/generate-report-stream - Streaming Analysis"""
    print_header("ENDPOINT 2: POST /api/describe/generate-report-stream - SSE Streaming")
    
    demo_data = {
        "title": "SSH Brute Force Attack - Web Servers",
        "description": "SSH brute force attack detected on 3 external-facing servers with over 50,000 login attempts in 6 hours. Attacker used credential stuffing with leaked username/password pairs from previous breaches.",
        "incident_type": "ddos",
        "severity": "high",
        "discovery_date": "2026-05-04T14:00:00Z",
        "current_status": "Ongoing"
    }
    
    print(f"{YELLOW}Demo Data:{RESET}")
    print(f"Title: {demo_data['title']}")
    print(f"Description length: {len(demo_data['description'])} chars\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/describe/generate-report-stream",
            json=demo_data,
            stream=True,
            timeout=60
        )
        success = response.status_code == 200
        
        print_test_result("POST /api/describe/generate-report-stream", response.status_code, success)
        
        if success:
            print(f"\n{YELLOW}Streaming Response (first 500 chars):{RESET}")
            chunk_count = 0
            full_response = ""
            for chunk in response.iter_lines():
                if chunk:
                    chunk_str = chunk.decode('utf-8') if isinstance(chunk, bytes) else chunk
                    if chunk_str.startswith('data: '):
                        chunk_text = chunk_str[6:]
                        full_response += chunk_text
                        chunk_count += 1
            
            print(f"Total chunks received: {chunk_count}")
            print(f"Total response length: {len(full_response)} chars")
            print(f"Preview: {full_response[:500]}...\n")
            return True
        else:
            print(f"{RED}Error: {response.text}{RESET}\n")
            return False
    except Exception as e:
        print(f"{RED}Exception: {str(e)}{RESET}\n")
        return False


def test_endpoint_3_recommend():
    """Test 3: POST /api/recommend - Action Recommendations"""
    print_header("ENDPOINT 3: POST /api/recommend - Actionable Recommendations")
    
    demo_data = {
        "incident_type": "ransomware",
        "severity": "critical",
        "description": "LockBit 3.0 ransomware has encrypted critical business files across file servers and encrypted backup systems. The attacker is demanding $500,000 for decryption keys and threatening to sell data."
    }
    
    print(f"{YELLOW}Demo Data:{RESET}")
    print(f"Incident Type: {demo_data['incident_type']}")
    print(f"Severity: {demo_data['severity']}")
    print(f"Description length: {len(demo_data['description'])} chars\n")
    
    try:
        response = requests.post(f"{BASE_URL}/recommend", json=demo_data, timeout=30)
        success = response.status_code == 200
        
        print_test_result("POST /api/recommend", response.status_code, success)
        
        if success:
            data = response.json()
            print(f"\n{YELLOW}Response Structure:{RESET}")
            print(f"  • status: {data.get('status')}")
            print(f"  • incident_type: {data.get('incident_type')}")
            print(f"  • severity: {data.get('severity')}")
            print(f"  • recommendation_count: {len(data.get('recommendations', []))}")
            
            print(f"\n{YELLOW}Recommendations:{RESET}")
            for i, rec in enumerate(data.get('recommendations', [])[:3], 1):
                print(f"\n  {i}. {rec.get('action_type')}")
                print(f"     Description: {rec.get('description')[:80]}...")
                print(f"     Priority: {rec.get('priority')}")
            
            print()
            return True
        else:
            print(f"{RED}Error: {response.text}{RESET}\n")
            return False
    except Exception as e:
        print(f"{RED}Exception: {str(e)}{RESET}\n")
        return False


def test_endpoint_4_analyse_single():
    """Test 4: POST /api/analyse/document - Single Document Analysis"""
    print_header("ENDPOINT 4: POST /api/analyse/document - Single Document Analysis")
    
    log_content = """2026-05-04T14:30:23.456Z [ERROR] Authentication failed for user 'finance_analyst@company.com' from IP 192.168.1.150
2026-05-04T14:31:45.123Z [WARN] Multiple failed login attempts from IP 203.0.113.42 (15 attempts in 2 minutes)
2026-05-04T14:32:01.789Z [ERROR] Unauthorized file access attempt: /var/data/financial_records/Q1_2026_balance.xlsx from user 'service_account'
2026-05-04T14:32:15.234Z [CRITICAL] Ransomware signature detected - process explorer.exe spawning suspicious child processes
2026-05-04T14:32:30.567Z [CRITICAL] Network anomaly: Large data exfiltration detected to external IP 198.51.100.55 (2.3GB in 5 minutes)
2026-05-04T14:32:45.890Z [ERROR] Database connection lost - backup replication failed
2026-05-04T14:33:01.234Z [CRITICAL] File server encryption detected - 5000+ files encrypted with .LOCKBIT extension
2026-05-04T14:33:15.678Z [ALERT] Emergency backup failed - ransomware has encrypted backup storage location"""
    
    demo_data = {
        "content": log_content,
        "doc_type": "log",
        "source": "security_monitoring_system",
        "priority": "critical"
    }
    
    print(f"{YELLOW}Demo Data:{RESET}")
    print(f"Document Type: {demo_data['doc_type']}")
    print(f"Source: {demo_data['source']}")
    print(f"Priority: {demo_data['priority']}")
    print(f"Content length: {len(demo_data['content'])} chars\n")
    
    try:
        response = requests.post(f"{BASE_URL}/analyse/document", json=demo_data, timeout=30)
        success = response.status_code == 200
        
        print_test_result("POST /api/analyse/document", response.status_code, success)
        
        if success:
            data = response.json()
            analysis = data.get('analysis', {})
            
            print(f"\n{YELLOW}Response Structure:{RESET}")
            print(f"  • status: {data.get('status')}")
            print(f"  • document_title: {analysis.get('document_title')}")
            print(f"  • summary: {analysis.get('summary')[:100]}...")
            print(f"  • findings_count: {len(analysis.get('findings', []))}")
            print(f"  • risk_level: {analysis.get('risk_assessment', {}).get('overall_risk_level')}")
            
            print(f"\n{YELLOW}Findings (first 2):{RESET}")
            for i, finding in enumerate(analysis.get('findings', [])[:2], 1):
                print(f"\n  {i}. {finding.get('title')}")
                print(f"     Type: {finding.get('finding_type')}")
                print(f"     Severity: {finding.get('severity')}")
                print(f"     Description: {finding.get('description')[:80]}...")
            
            print()
            return True
        else:
            print(f"{RED}Error: {response.text}{RESET}\n")
            return False
    except Exception as e:
        print(f"{RED}Exception: {str(e)}{RESET}\n")
        return False


def test_endpoint_5_analyse_bulk():
    """Test 5: POST /api/analyse/document/bulk - Bulk Document Analysis"""
    print_header("ENDPOINT 5: POST /api/analyse/document/bulk - Bulk Analysis (max 10)")
    
    documents = [
        {
            "content": "CRITICAL: SQL injection vulnerability discovered in user login form. Input validation missing on 'username' parameter. Allows unauthenticated database access.",
            "doc_type": "alert",
            "source": "vulnerability_scanner"
        },
        {
            "content": "Configuration review: API keys stored in plaintext in config.ini file. Encryption keys accessible to all users with file server access. Database passwords embedded in application source code.",
            "doc_type": "configuration",
            "source": "security_audit"
        },
        {
            "content": "Compliance gap: GDPR data retention policy not enforced. Customer personal data retained for 5 years instead of required 1 year. No automated deletion implemented.",
            "doc_type": "policy",
            "source": "compliance_team"
        }
    ]
    
    demo_data = {"documents": documents}
    
    print(f"{YELLOW}Demo Data:{RESET}")
    print(f"Document count: {len(documents)}")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc['doc_type']} from {doc['source']}")
    print()
    
    try:
        response = requests.post(f"{BASE_URL}/analyse/document/bulk", json=demo_data, timeout=60)
        success = response.status_code == 200
        
        print_test_result("POST /api/analyse/document/bulk", response.status_code, success)
        
        if success:
            data = response.json()
            summary = data.get('summary', {})
            
            print(f"\n{YELLOW}Response Structure:{RESET}")
            print(f"  • status: {data.get('status')}")
            print(f"  • bulk_analysis_id: {data.get('bulk_analysis_id')}")
            print(f"  • results_count: {len(data.get('results', []))}")
            print(f"  • total_documents: {summary.get('total_documents')}")
            print(f"  • successful_analyses: {summary.get('successful_analyses')}")
            print(f"  • failed_analyses: {summary.get('failed_analyses')}")
            print(f"  • total_findings: {summary.get('total_findings')}")
            
            print(f"\n{YELLOW}Per-Document Results:{RESET}")
            for i, result in enumerate(data.get('results', [])[:3], 1):
                print(f"\n  {i}. Document {result.get('index')} - {result.get('status')}")
                if result.get('status') == 'success':
                    analysis = result.get('analysis', {})
                    print(f"     Title: {analysis.get('document_title')}")
                    print(f"     Findings: {len(analysis.get('findings', []))}")
            
            print()
            return True
        else:
            print(f"{RED}Error: {response.text}{RESET}\n")
            return False
    except Exception as e:
        print(f"{RED}Exception: {str(e)}{RESET}\n")
        return False


def test_endpoint_6_batch():
    """Test 6: POST /api/batch/process - Batch Processing"""
    print_header("ENDPOINT 6: POST /api/batch/process - Batch Item Processing")
    
    batch_items = [
        {
            "id": "incident_001",
            "content": "Unusual spike in failed login attempts from internal IP 10.0.1.50 targeting database admin accounts. 1200+ attempts in 30 minutes.",
            "type": "log",
            "source": "security_log_aggregator",
            "priority": "high"
        },
        {
            "id": "incident_002",
            "content": "Potential insider threat: Employee account used to download 50GB of customer database to external storage after hours.",
            "type": "alert",
            "source": "dlp_system",
            "priority": "critical"
        },
        {
            "id": "incident_003",
            "content": "Misconfiguration detected: S3 bucket public-data-backup configured with public read/write permissions. Contains 10GB of unencrypted customer PII.",
            "type": "document",
            "source": "cloud_security_scanner",
            "priority": "critical"
        },
        {
            "id": "incident_004",
            "content": "Malware detected: 15 systems infected with trojan.generic.12345. C2 communication to 203.0.113.10:4444 detected on all infected hosts.",
            "type": "alert",
            "source": "endpoint_protection",
            "priority": "critical"
        }
    ]
    
    demo_data = {
        "items": batch_items,
        "parallel": False,
        "timeout": 300000
    }
    
    print(f"{YELLOW}Demo Data:{RESET}")
    print(f"Item count: {len(batch_items)}")
    for item in batch_items:
        print(f"  • {item['id']}: {item['type']} (priority: {item['priority']})")
    print(f"Parallel processing: {demo_data['parallel']}")
    print(f"Timeout: {demo_data['timeout']}ms\n")
    
    try:
        response = requests.post(f"{BASE_URL}/batch/process", json=demo_data, timeout=120)
        success = response.status_code == 200
        
        print_test_result("POST /api/batch/process", response.status_code, success)
        
        if success:
            data = response.json()
            summary = data.get('summary', {})
            
            print(f"\n{YELLOW}Response Structure:{RESET}")
            print(f"  • status: {data.get('status')}")
            print(f"  • batch_id: {data.get('batch_id')}")
            print(f"  • total_items: {summary.get('total_items')}")
            print(f"  • successful: {summary.get('successful')}")
            print(f"  • failed: {summary.get('failed')}")
            print(f"  • total_time_ms: {summary.get('total_time_ms')}")
            print(f"  • average_time_per_item_ms: {summary.get('average_time_per_item_ms')}")
            
            print(f"\n{YELLOW}Processing Results (first 2 items):{RESET}")
            for i, result in enumerate(data.get('results', [])[:2], 1):
                print(f"\n  {i}. Item {result.get('id')} - {result.get('status')}")
                print(f"     Index: {result.get('index')}")
                print(f"     Type: {result.get('type')}")
                if result.get('status') == 'success':
                    print(f"     Processing time: {result.get('processing_time_ms')}ms")
                else:
                    print(f"     Error: {result.get('error')}")
            
            print(f"\n{YELLOW}Metadata:{RESET}")
            metadata = data.get('metadata', {})
            print(f"  • batch_size: {metadata.get('batch_size')}")
            print(f"  • max_batch_size: {metadata.get('max_batch_size')}")
            print(f"  • delay_per_item_ms: {metadata.get('delay_per_item_ms')}")
            print(f"  • parallel_processing: {metadata.get('parallel_processing')}")
            
            print()
            return True
        else:
            print(f"{RED}Error: {response.text}{RESET}\n")
            return False
    except Exception as e:
        print(f"{RED}Exception: {str(e)}{RESET}\n")
        return False


def test_error_handling():
    """Test Error Handling and Edge Cases"""
    print_header("ERROR HANDLING & EDGE CASES")
    
    test_cases = [
        {
            "name": "Missing required field",
            "endpoint": "/describe",
            "data": {"title": "Test"},  # Missing description
            "expected_code": 400
        },
        {
            "name": "Empty items array",
            "endpoint": "/batch/process",
            "data": {"items": []},
            "expected_code": 400
        },
        {
            "name": "Batch exceeds limit",
            "endpoint": "/batch/process",
            "data": {"items": [{"content": f"Item {i}"} for i in range(25)]},
            "expected_code": 400
        },
        {
            "name": "Invalid incident type",
            "endpoint": "/recommend",
            "data": {
                "incident_type": "invalid_type",
                "severity": "high",
                "description": "Test"
            },
            "expected_code": 400
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}{test_case['endpoint']}",
                json=test_case['data'],
                timeout=10
            )
            is_expected = response.status_code == test_case['expected_code']
            status = f"{GREEN}✓{RESET}" if is_expected else f"{RED}✗{RESET}"
            
            print(f"{status} {test_case['name']:<40} Got {response.status_code} (expected {test_case['expected_code']})")
            
            if is_expected:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"{RED}✗ {test_case['name']:<40} Exception: {str(e)[:50]}{RESET}")
            failed += 1
    
    print(f"\n{YELLOW}Error Handling Results: {passed} passed, {failed} failed{RESET}\n")
    return failed == 0


def test_response_format_validation():
    """Validate response formats against API spec"""
    print_header("RESPONSE FORMAT VALIDATION")
    
    # Test describe endpoint response structure
    describe_response = requests.post(
        f"{BASE_URL}/describe",
        json={"description": "Test incident for format validation"},
        timeout=30
    )
    
    if describe_response.status_code == 200:
        data = describe_response.json()
        required_fields = ["status", "title", "analysis", "generated_at", "metadata"]
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            print(f"{RED}✗ /describe missing fields: {missing}{RESET}")
            return False
        else:
            print(f"{GREEN}✓ /describe has all required fields{RESET}")
            return True
    else:
        print(f"{RED}✗ /describe returned {describe_response.status_code}{RESET}")
        return False


def main():
    """Run all QA tests"""
    print(f"\n{BOLD}{BLUE}")
    print("╔════════════════════════════════════════════════════════════════════════════════╗")
    print("║             COMPREHENSIVE QA TESTING - ALL 6 ENDPOINTS                         ║")
    print("║                       Professional Demo Data Suite                             ║")
    print("║                          May 4, 2026 - Final QA                                ║")
    print("╚════════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    
    print(f"{YELLOW}Waiting for service to be ready...{RESET}")
    time.sleep(2)
    
    # Check health
    try:
        health = requests.get("http://localhost:5000/health", timeout=5)
        if health.status_code != 200:
            print(f"{RED}Service health check failed{RESET}")
            return
    except:
        print(f"{YELLOW}Waiting for service startup...{RESET}")
        time.sleep(3)
    
    results = []
    
    # Run all endpoint tests
    results.append(("Endpoint 1: Describe", test_endpoint_1_describe()))
    results.append(("Endpoint 2: Stream", test_endpoint_2_stream()))
    results.append(("Endpoint 3: Recommend", test_endpoint_3_recommend()))
    results.append(("Endpoint 4: Analyse Single", test_endpoint_4_analyse_single()))
    results.append(("Endpoint 5: Analyse Bulk", test_endpoint_5_analyse_bulk()))
    results.append(("Endpoint 6: Batch", test_endpoint_6_batch()))
    
    # Test error handling
    error_handling_ok = test_error_handling()
    results.append(("Error Handling", error_handling_ok))
    
    # Validate response formats
    format_ok = test_response_format_validation()
    results.append(("Response Format", format_ok))
    
    # Print summary
    print_header("QA TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"{test_name:<40} {status}")
    
    print(f"\n{BOLD}Overall Result: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"{GREEN}All endpoints are professional and demo-ready!{RESET}\n")
    else:
        print(f"{RED}Some tests failed. See details above.{RESET}\n")


if __name__ == "__main__":
    main()
