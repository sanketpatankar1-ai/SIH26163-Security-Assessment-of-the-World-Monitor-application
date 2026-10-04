"""
security_engine/scanner.py
============================
Main Assessment Orchestrator

This is the central scanner that:
  1. Accepts a target URL
  2. Runs all check modules in sequence
  3. Collects and deduplicates findings
  4. Calculates the security score
  5. Returns a structured assessment result

Usage:
  from security_engine.scanner import run_assessment
  result = run_assessment("http://localhost:5001")
"""

import datetime
from typing import Optional
from .finding import Finding, FindingSource, calculate_security_score
from .auth_checks import run_auth_checks
from .authorization_checks import run_authorization_checks
from .api_checks import run_api_checks
from .input_validation_checks import run_input_validation_checks
from .communication_checks import run_communication_checks
from .client_security_checks import run_client_security_checks
from .storage_checks import run_storage_checks
from .demo_data import get_demo_findings


# Assessment module registry — easy to add new check categories
ASSESSMENT_MODULES = [
    ("Authentication",           run_auth_checks),
    ("Authorization",            run_authorization_checks),
    ("API Security",             run_api_checks),
    ("Input Validation",         run_input_validation_checks),
    ("Communication Security",   run_communication_checks),
    ("Client-Side Security",     run_client_security_checks),
    ("Data Storage & Privacy",   run_storage_checks),
]


def run_assessment(
    target_url: str = "http://localhost:5001",
    include_demo: bool = False,
) -> dict:
    """
    Run the full security assessment against the target URL.

    Args:
        target_url:    URL of the application to assess
        include_demo:  Whether to include demo/sample findings alongside real ones

    Returns:
        A structured assessment result dict with findings and score.
    """
    started_at = datetime.datetime.utcnow().isoformat()
    all_findings: list[Finding] = []
    module_results = []

    print(f"\n{'='*60}")
    print(f"  SIH26163 — Security Assessment Engine")
    print(f"  Target: {target_url}")
    print(f"  Started: {started_at}")
    print(f"{'='*60}\n")

    # Run each check module
    for module_name, check_fn in ASSESSMENT_MODULES:
        print(f"  [{module_name}] Running checks...")
        try:
            findings = check_fn(target_url)
            all_findings.extend(findings)
            module_results.append({
                "module": module_name,
                "findings_count": len(findings),
                "status": "completed",
            })
            print(f"  [{module_name}] Found {len(findings)} issue(s)")
        except Exception as e:
            module_results.append({
                "module": module_name,
                "findings_count": 0,
                "status": f"error: {str(e)}",
            })
            print(f"  [{module_name}] Error: {e}")

    # Optionally add demo findings
    if include_demo:
        demo = get_demo_findings()
        # Only add demo findings that don't conflict with real findings
        real_ids = {f.id for f in all_findings}
        for d in demo:
            d.id = f"DEMO-{d.id}"  # Prefix to avoid ID conflicts
            if d.id not in real_ids:
                all_findings.append(d)

    completed_at = datetime.datetime.utcnow().isoformat()

    # Calculate security score
    score_data = calculate_security_score(all_findings)

    print(f"\n  Assessment Complete!")
    print(f"  Total findings: {len(all_findings)}")
    print(f"  Security Score: {score_data['score']}/100 ({score_data['grade']})")
    print(f"{'='*60}\n")

    return {
        "assessment_id": f"ASSESS-{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        "target_url": target_url,
        "started_at": started_at,
        "completed_at": completed_at,
        "findings": [f.to_dict() for f in all_findings],
        "score": score_data,
        "module_results": module_results,
        "status": "completed",
        "disclaimer": (
            "This assessment was performed against a controlled prototype target. "
            "Findings marked 'Demo' are representative samples. "
            "This is not an industry-certified security rating."
        ),
    }
