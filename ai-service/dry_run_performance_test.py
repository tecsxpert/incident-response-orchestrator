#!/usr/bin/env python3
"""
Dry Run Performance Test - All 6 Endpoints with Groq API
Tests all endpoints with real Groq API and records detailed response times
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys

# Base URL for the service
BASE_URL = "http://localhost:5000"

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

class PerformanceMetrics:
    """Track performance metrics for each endpoint"""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
    
    def add_result(self, endpoint: str, scenario: str, status_code: int, 
                   response_time_ms: float, response_size_bytes: int, 
                   success: bool, details: str = ""):
        """Add a test result"""
        result = {
            "endpoint": endpoint,
            "scenario": scenario,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "response_size_bytes": response_size_bytes,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        successful = [r for r in self.results if r["success"]]
        failed = [r for r in self.results if not r["success"]]
        
        response_times = [r["response_time_ms"] for r in successful]
        response_sizes = [r["response_size_bytes"] for r in successful]
        
        return {
            "total_tests": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": f"{(len(successful) / len(self.results) * 100):.1f}%",
            "avg_response_time_ms": f"{sum(response_times) / len(response_times):.1f}" if response_times else "N/A",
            "min_response_time_ms": f"{min(response_times):.1f}" if response_times else "N/A",
            "max_response_time_ms": f"{max(response_times):.1f}" if response_times else "N/A",
            "median_response_time_ms": f"{sorted(response_times)[len(response_times)//2]:.1f}" if response_times else "N/A",
            "total_data_transferred_mb": f"{sum(response_sizes) / (1024*1024):.2f}",
            "test_duration_seconds": (datetime.now() - self.start_time).total_seconds()
        }


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def print_test(num: int, endpoint: str, scenario: str):
    """Print test start"""
    print(f"{BOLD}{YELLOW}Test {num}: {endpoint}{RESET}")
    print(f"  Scenario: {scenario}")
    print(f"  ", end="", flush=True)


def print_result(success: bool, response_time_ms: float, status_code: int, size_bytes: int):
    """Print test result"""
    status_icon = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
    print(f"{status_icon} {response_time_ms:.1f}ms | HTTP {status_code} | {size_bytes} bytes")


# Test 1: POST /api/describe
def test_endpoint_1_describe(metrics: PerformanceMetrics) -> bool:
    """Test comprehensive incident analysis endpoint"""
    print_test(1, "POST /api/describe", "Ransomware Attack Analysis")
    
    payload = {
        "title": "Critical Ransomware Attack - Finance Department",
        "incident_type": "ransomware",
        "severity": "critical",
        "description": """
        LockBit 3.0 ransomware detected on Finance Department network. 
        Attack vector: Phishing email with Excel macro.
        Impact: 850GB of financial records encrypted.
        Ransom demand: $500,000 in cryptocurrency.
        Infrastructure: 45 workstations on segmented finance network.
        Initial compromise time: 02:30 UTC
        Detection time: 08:15 UTC (5h45m dwell time)
        Backup systems: Appear to be compromised as well.
        """
    }
    
    try:
        start = time.time()
        response = requests.post(f"{BASE_URL}/api/describe", json=payload, timeout=30)
        elapsed_ms = (time.time() - start) * 1000
        
        success = response.status_code == 200
        response_size = len(response.text)
        
        print_result(success, elapsed_ms, response.status_code, response_size)
        
        if success:
            data = response.json()
            details = f"Analysis: {len(data.get('analysis', ''))} chars"
        else:
            details = response.text[:100]
        
        metrics.add_result("POST /api/describe", "Ransomware Analysis", 
                          response.status_code, elapsed_ms, response_size, success, details)
        return success
    except Exception as e:
        print(f"{RED}✗ ERROR{RESET}")
        metrics.add_result("POST /api/describe", "Ransomware Analysis", 
                          0, 0, 0, False, str(e))
        return False


# Test 2: POST /api/describe/generate-report-stream
def test_endpoint_2_stream(metrics: PerformanceMetrics) -> bool:
    """Test streaming report generation endpoint"""
    print_test(2, "POST /api/describe/generate-report-stream", "SSH Brute Force (SSE Stream)")
    
    payload = {
        "title": "SSH Brute Force Attack - Web Servers",
        "incident_type": "ddos",
        "severity": "high",
        "description": """
        SSH Brute Force attack detected on web servers.
        50,000+ login attempts in 6 hours from external IP ranges.
        Attack vector: Credential stuffing with leaked password pairs.
        3 external-facing web servers targeted (10.0.1.5, 10.0.1.6, 10.0.1.7).
        Successful logins: 0 (so far)
        Failed attempts: 50,847 across all servers.
        Attack source: Multiple IP addresses from compromised botnet.
        """
    }
    
    try:
        start = time.time()
        response = requests.post(f"{BASE_URL}/api/describe/generate-report-stream", 
                                json=payload, timeout=30, stream=True)
        
        # Consume the stream
        total_chunks = 0
        total_data = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                total_chunks += 1
                total_data += len(chunk)
        
        elapsed_ms = (time.time() - start) * 1000
        
        success = response.status_code == 200
        
        print_result(success, elapsed_ms, response.status_code, total_data)
        
        details = f"Stream: {total_chunks} chunks, {total_data} bytes"
        metrics.add_result("POST /api/describe/stream", "SSH Brute Force (Stream)", 
                          response.status_code, elapsed_ms, total_data, success, details)
        return success
    except Exception as e:
        print(f"{RED}✗ ERROR{RESET}")
        metrics.add_result("POST /api/describe/stream", "SSH Brute Force (Stream)", 
                          0, 0, 0, False, str(e))
        return False


# Test 3: POST /api/recommend
def test_endpoint_3_recommend(metrics: PerformanceMetrics) -> bool:
    """Test recommendation endpoint"""
    print_test(3, "POST /api/recommend", "Ransomware Response Recommendations")
    
    payload = {
        "incident_type": "ransomware",
        "severity": "critical",
        "description": """
        LockBit 3.0 ransomware with 850GB encrypted data.
        $500k ransom demand.
        45 workstations compromised.
        Backup systems potentially compromised.
        5+ hour dwell time before detection.
        """
    }
    
    try:
        start = time.time()
        response = requests.post(f"{BASE_URL}/api/recommend", json=payload, timeout=30)
        elapsed_ms = (time.time() - start) * 1000
        
        success = response.status_code == 200
        response_size = len(response.text)
        
        print_result(success, elapsed_ms, response.status_code, response_size)
        
        if success:
            data = response.json()
            rec_count = len(data.get('recommendations', []))
            details = f"Recommendations: {rec_count}"
        else:
            details = response.text[:100]
        
        metrics.add_result("POST /api/recommend", "Ransomware Recommendations", 
                          response.status_code, elapsed_ms, response_size, success, details)
        return success
    except Exception as e:
        print(f"{RED}✗ ERROR{RESET}")
        metrics.add_result("POST /api/recommend", "Ransomware Recommendations", 
                          0, 0, 0, False, str(e))
        return False


# Test 4: POST /api/analyse/document
def test_endpoint_4_analyse_single(metrics: PerformanceMetrics) -> bool:
    """Test single document analysis endpoint"""
    print_test(4, "POST /api/analyse/document", "Security Event Log Analysis")
    
    payload = {
        "document_type": "log",
        "source": "security_monitoring_system",
        "priority": "critical",
        "content": """
        2026-05-04 02:30:15 - ALERT: Suspicious PowerShell execution from user jsmith
        2026-05-04 02:31:42 - ERROR: Authentication failure for admin account from 192.168.1.105
        2026-05-04 02:33:08 - ALERT: File access anomaly - large data read from backup share
        2026-05-04 02:45:19 - WARNING: Process explorer.exe spawning suspicious child processes
        2026-05-04 03:12:33 - ALERT: Ransomware signature detected - .LOCKBIT file extension
        2026-05-04 04:56:22 - CRITICAL: Backup system drive mapped and accessed
        2026-05-04 07:43:11 - ERROR: Multiple failed authentication attempts (847 attempts)
        2026-05-04 08:15:03 - ALERT: Incident response automated alert triggered
        """
    }
    
    try:
        start = time.time()
        response = requests.post(f"{BASE_URL}/api/analyse/document", json=payload, timeout=30)
        elapsed_ms = (time.time() - start) * 1000
        
        success = response.status_code == 200
        response_size = len(response.text)
        
        print_result(success, elapsed_ms, response.status_code, response_size)
        
        if success:
            data = response.json()
            findings = len(data.get('analysis', {}).get('findings', []))
            details = f"Findings: {findings}"
        else:
            details = response.text[:100]
        
        metrics.add_result("POST /api/analyse/document", "Security Event Log Analysis", 
                          response.status_code, elapsed_ms, response_size, success, details)
        return success
    except Exception as e:
        print(f"{RED}✗ ERROR{RESET}")
        metrics.add_result("POST /api/analyse/document", "Security Event Log Analysis", 
                          0, 0, 0, False, str(e))
        return False


# Test 5: POST /api/analyse/document/bulk
def test_endpoint_5_analyse_bulk(metrics: PerformanceMetrics) -> bool:
    """Test bulk document analysis endpoint"""
    print_test(5, "POST /api/analyse/document/bulk", "Multi-Document Analysis (3 docs)")
    
    payload = {
        "documents": [
            {
                "document_type": "alert",
                "source": "vulnerability_scanner",
                "priority": "critical",
                "content": "SQL Injection vulnerability detected in user login form. Input validation missing. Unauthenticated database access possible."
            },
            {
                "document_type": "configuration",
                "source": "security_audit",
                "priority": "high",
                "content": "Configuration review found: plaintext credentials in config files, unencrypted API keys in environment, weak database password policies."
            },
            {
                "document_type": "policy",
                "source": "compliance_team",
                "priority": "high",
                "content": "GDPR compliance gap: Data retention policy requires 1-year deletion but systems retain data for 5 years. No automated deletion implemented."
            }
        ]
    }
    
    try:
        start = time.time()
        response = requests.post(f"{BASE_URL}/api/analyse/document/bulk", json=payload, timeout=60)
        elapsed_ms = (time.time() - start) * 1000
        
        success = response.status_code == 200
        response_size = len(response.text)
        
        print_result(success, elapsed_ms, response.status_code, response_size)
        
        if success:
            data = response.json()
            doc_count = len(data.get('results', []))
            details = f"Documents analyzed: {doc_count}"
        else:
            details = response.text[:100]
        
        metrics.add_result("POST /api/analyse/bulk", "Multi-Document Analysis", 
                          response.status_code, elapsed_ms, response_size, success, details)
        return success
    except Exception as e:
        print(f"{RED}✗ ERROR{RESET}")
        metrics.add_result("POST /api/analyse/bulk", "Multi-Document Analysis", 
                          0, 0, 0, False, str(e))
        return False


# Test 6: POST /api/batch/process
def test_endpoint_6_batch(metrics: PerformanceMetrics) -> bool:
    """Test batch processing endpoint"""
    print_test(6, "POST /api/batch/process", "Batch Processing (4 incidents)")
    
    payload = {
        "items": [
            {
                "id": "incident_001",
                "type": "log",
                "source": "security_system",
                "priority": "high",
                "content": "Brute force attack detected on SSH service with 1000+ failed login attempts from single IP address."
            },
            {
                "id": "incident_002",
                "type": "alert",
                "source": "dlp_system",
                "priority": "critical",
                "content": "Insider threat: Employee account downloading 50GB customer database after business hours. Unauthorized access detected."
            },
            {
                "id": "incident_003",
                "type": "alert",
                "source": "cloud_security",
                "priority": "critical",
                "content": "Misconfigured S3 bucket with public read/write permissions. 10GB unencrypted customer PII exposed publicly."
            },
            {
                "id": "incident_004",
                "type": "alert",
                "source": "endpoint_protection",
                "priority": "critical",
                "content": "Endpoint malware: 15 systems infected with trojan.generic.12345. C2 communication to external IP:port detected. All infected hosts communicating."
            }
        ]
    }
    
    try:
        start = time.time()
        response = requests.post(f"{BASE_URL}/api/batch/process", json=payload, timeout=120)
        elapsed_ms = (time.time() - start) * 1000
        
        success = response.status_code == 200
        response_size = len(response.text)
        
        print_result(success, elapsed_ms, response.status_code, response_size)
        
        if success:
            data = response.json()
            processed = len(data.get('results', []))
            details = f"Items processed: {processed}/4"
        else:
            details = response.text[:100]
        
        metrics.add_result("POST /api/batch/process", "Batch Processing (4 items)", 
                          response.status_code, elapsed_ms, response_size, success, details)
        return success
    except Exception as e:
        print(f"{RED}✗ ERROR{RESET}")
        metrics.add_result("POST /api/batch/process", "Batch Processing (4 items)", 
                          0, 0, 0, False, str(e))
        return False


def main():
    """Run all dry run tests"""
    print_header("AI SERVICE DRY RUN - PERFORMANCE TEST")
    print(f"Start Time: {datetime.now().isoformat()}")
    print(f"Base URL: {BASE_URL}")
    print(f"Service Status: Checking...\n")
    
    # Check service availability
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 404:  # 404 is expected for undefined /health
            print(f"{GREEN}✓ Service is responding{RESET}\n")
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ Cannot connect to service at {BASE_URL}{RESET}")
        print(f"Make sure the Flask service is running: python app.py\n")
        sys.exit(1)
    except Exception as e:
        print(f"{YELLOW}⚠ Service check inconclusive: {e}{RESET}\n")
    
    metrics = PerformanceMetrics()
    
    print(f"{BOLD}Running Performance Tests:{RESET}\n")
    
    # Run all tests
    test_1_ok = test_endpoint_1_describe(metrics)
    print()
    test_2_ok = test_endpoint_2_stream(metrics)
    print()
    test_3_ok = test_endpoint_3_recommend(metrics)
    print()
    test_4_ok = test_endpoint_4_analyse_single(metrics)
    print()
    test_5_ok = test_endpoint_5_analyse_bulk(metrics)
    print()
    test_6_ok = test_endpoint_6_batch(metrics)
    
    # Print summary
    print_header("PERFORMANCE SUMMARY")
    
    summary = metrics.get_summary()
    
    print(f"{BOLD}Overall Results:{RESET}")
    print(f"  Tests Run:           {summary['total_tests']}")
    print(f"  Successful:          {summary['successful']}")
    print(f"  Failed:              {summary['failed']}")
    print(f"  Success Rate:        {summary['success_rate']}")
    
    print(f"\n{BOLD}Response Time Metrics:{RESET}")
    print(f"  Average:             {summary['avg_response_time_ms']} ms")
    print(f"  Minimum:             {summary['min_response_time_ms']} ms")
    print(f"  Maximum:             {summary['max_response_time_ms']} ms")
    print(f"  Median:              {summary['median_response_time_ms']} ms")
    
    print(f"\n{BOLD}Data Transfer:{RESET}")
    print(f"  Total:               {summary['total_data_transferred_mb']} MB")
    
    print(f"\n{BOLD}Test Duration:{RESET}")
    print(f"  Total Time:          {summary['test_duration_seconds']:.1f} seconds")
    
    # Endpoint breakdown
    print(f"\n{BOLD}Endpoint Breakdown:{RESET}\n")
    
    endpoints_tested = {}
    for result in metrics.results:
        ep = result['endpoint']
        if ep not in endpoints_tested:
            endpoints_tested[ep] = []
        endpoints_tested[ep].append(result)
    
    for ep, results in endpoints_tested.items():
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        times = [r['response_time_ms'] for r in results if r['success']]
        avg_time = sum(times) / len(times) if times else 0
        
        status = f"{GREEN}✓{RESET}" if successful == total else f"{RED}✗{RESET}"
        print(f"  {status} {ep}")
        print(f"     Success: {successful}/{total} | Avg Time: {avg_time:.1f}ms")
    
    # Detailed results
    print(f"\n{BOLD}Detailed Results:{RESET}\n")
    
    for i, result in enumerate(metrics.results, 1):
        status = f"{GREEN}✓ PASS{RESET}" if result['success'] else f"{RED}✗ FAIL{RESET}"
        print(f"{i}. {status} - {result['endpoint']}")
        print(f"   Scenario:        {result['scenario']}")
        print(f"   Response Time:   {result['response_time_ms']:.1f} ms")
        print(f"   Status Code:     {result['status_code']}")
        print(f"   Response Size:   {result['response_size_bytes']} bytes")
        print(f"   Details:         {result['details']}")
        print()
    
    # Save results to JSON
    output_file = "dry_run_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "results": metrics.results
        }, f, indent=2)
    
    print(f"{BOLD}Results saved to: {output_file}{RESET}\n")
    
    # Final status
    if summary['failed'] == 0:
        print(f"{GREEN}{BOLD}✓ ALL TESTS PASSED - SERVICE READY FOR PRODUCTION{RESET}\n")
        return 0
    else:
        print(f"{YELLOW}{BOLD}⚠ SOME TESTS FAILED - REVIEW REQUIRED{RESET}\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
