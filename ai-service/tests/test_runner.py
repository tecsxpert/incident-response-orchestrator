"""Automated test runner for incident analysis prompt quality validation."""

import sys
import os
import json
import time
import logging
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.groq_client import GroqClient
from prompts.templates import SYSTEM_PROMPT
from tests.test_describe_cases import TEST_CASES, QUALITY_CRITERIA


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DescribeEndpointTester:
    """Tester for describe endpoint with quality validation."""

    def __init__(self):
        """Initialize tester."""
        try:
            self.client = GroqClient()
            logger.info("Groq client initialized successfully")
        except ValueError as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            raise

    def _evaluate_quality(self, analysis: str) -> dict:
        """Evaluate analysis quality using scoring algorithm.
        
        Args:
            analysis: The analysis text to evaluate
            
        Returns:
            dict with score and details
        """
        score = 0
        details = []

        # Check for required sections (50 points)
        sections_found = 0
        for section in QUALITY_CRITERIA["structure"]["sections"]:
            if section.lower() in analysis.lower():
                sections_found += 1
        section_score = int((sections_found / len(QUALITY_CRITERIA["structure"]["sections"])) * 50)
        score += section_score
        details.append(f"Structure: {sections_found}/{len(QUALITY_CRITERIA['structure']['sections'])} sections ({section_score} pts)")

        # Check for technical accuracy (20 points)
        technical_terms = ["CVSS", "MITRE", "ATT&CK", "severity", "impact", "NIST", "containment", "forensic", "remediation"]
        terms_found = sum(1 for term in technical_terms if term.lower() in analysis.lower())
        technical_score = int((terms_found / len(technical_terms)) * 20)
        score += technical_score
        details.append(f"Technical Accuracy: {terms_found}/{len(technical_terms)} terms ({technical_score} pts)")

        # Check formatting (15 points)
        formatting_score = 0
        if "##" in analysis:
            formatting_score += 5
        if "**" in analysis or "*" in analysis:
            formatting_score += 5
        if len(analysis) > 1000:
            formatting_score += 5
        score += formatting_score
        details.append(f"Formatting: {formatting_score} pts")

        # Check for professional terminology (10 points)
        professional_terms = ["vulnerability", "exploit", "malware", "threat", "risk", "confidentiality", "integrity", "availability"]
        prof_terms_found = sum(1 for term in professional_terms if term.lower() in analysis.lower())
        prof_score = int((prof_terms_found / len(professional_terms)) * 10)
        score += prof_score
        details.append(f"Terminology: {prof_terms_found}/{len(professional_terms)} terms ({prof_score} pts)")

        # Actionability check (5 points)
        if "recommend" in analysis.lower() or "should" in analysis.lower() or "action" in analysis.lower():
            score += 5
            details.append("Actionability: 5 pts")

        # Penalty for vagueness (max -5 points)
        vague_words = analysis.count("may") + analysis.count("possibly") + analysis.count("might")
        if vague_words > 10:
            penalty = min(5, vague_words - 10)
            score -= penalty
            details.append(f"Penalty for vagueness: -{penalty} pts")

        return {
            "score": max(0, min(100, score)),
            "details": details,
            "max_score": 100
        }

    def test_case(self, case_num: int, test_case: dict) -> dict:
        """Execute a single test case.
        
        Args:
            case_num: Test case number
            test_case: Test case dictionary
            
        Returns:
            dict with test results
        """
        print(f"\n{'='*80}")
        print(f"EXECUTING: {test_case['name']}")
        print(f"{'='*80}")

        start_time = time.time()

        try:
            # Call the analyze_incident endpoint
            analysis = self.client.analyze_incident(
                incident_description=test_case["description"],
                context=test_case["context"],
                system_prompt=SYSTEM_PROMPT,
                title=test_case["title"]
            )

            end_time = time.time()
            duration = end_time - start_time

            # Evaluate quality
            quality = self._evaluate_quality(analysis)

            # Determine pass/fail
            passed = quality["score"] >= 75
            status = "✅ PASSED" if passed else "❌ FAILED"

            print(f"\n{status} - Quality Score: {quality['score']}/100")
            print(f"Duration: {duration:.2f} seconds")
            print("\nQuality Breakdown:")
            for detail in quality["details"]:
                print(f"  - {detail}")

            print(f"\nAnalysis Preview (first 500 chars):")
            print("-" * 80)
            print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
            print("-" * 80)

            return {
                "case_num": case_num,
                "name": test_case["name"],
                "status": "passed" if passed else "failed",
                "quality_score": quality["score"],
                "duration": duration,
                "quality_details": quality["details"],
                "analysis_length": len(analysis),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error in test case {case_num}: {str(e)}")
            return {
                "case_num": case_num,
                "name": test_case["name"],
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def run_all_tests(self) -> list:
        """Run all test cases with delays between API calls.
        
        Returns:
            list of test results
        """
        logger.info(f"Starting test suite with {len(TEST_CASES)} test cases")
        results = []

        for idx, test_case in enumerate(TEST_CASES, 1):
            result = self.test_case(idx, test_case)
            results.append(result)

            # Add delay between API calls (2 seconds)
            if idx < len(TEST_CASES):
                print(f"\n⏳ Waiting 2 seconds before next test...\n")
                time.sleep(2)

        return results

    def save_results(self, filename: str = "test_results.json") -> str:
        """Save test results to JSON file.
        
        Args:
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        results = self.run_all_tests()

        # Calculate summary
        passed = sum(1 for r in results if r.get("status") == "passed")
        failed = sum(1 for r in results if r.get("status") == "failed")
        errors = sum(1 for r in results if r.get("status") == "error")
        avg_score = sum(r.get("quality_score", 0) for r in results) / len([r for r in results if r.get("quality_score")]) if any(r.get("quality_score") for r in results) else 0

        summary = {
            "test_suite": "Incident Analysis Prompt Quality Validation",
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "average_quality_score": round(avg_score, 2),
            "pass_rate": round((passed / len(results)) * 100, 2) if results else 0,
            "results": results
        }

        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Results saved to {filepath}")

        # Print summary
        print(f"\n{'='*80}")
        print("TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Errors: {summary['errors']}")
        print(f"Pass Rate: {summary['pass_rate']}%")
        print(f"Average Quality Score: {summary['average_quality_score']}/100")
        print(f"Results saved to: {filepath}")
        print(f"{'='*80}\n")

        return filepath


def main():
    """Main entry point."""
    try:
        tester = DescribeEndpointTester()
        tester.save_results()
    except Exception as e:
        logger.error(f"Test suite failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
