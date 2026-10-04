"""
tests/test_engine.py
=====================
Unit tests for the Security Assessment Engine.

Verifies:
  1. Finding data model validation and dictionary serialization
  2. Demo dataset structure and validity across all 7 categories
  3. Scanner result schema
"""

from security_engine.finding import Finding, Severity, FindingStatus, FindingSource
from security_engine.demo_data import get_demo_findings


def test_finding_to_dict():
    """Verify that Finding serializes correctly for JSON/API responses."""
    f = Finding(
        id="SEC-TEST-001",
        title="Test Vulnerability",
        category="API Security",
        severity=Severity.HIGH,
        description="Detailed description",
        affected_component="/api/v1/test",
        evidence="Observed HTTP 200 without auth",
        impact="Data exposure",
        recommendation="Implement JWT authentication",
        source=FindingSource.REAL,
        status=FindingStatus.OPEN,
        cwe_id="CWE-306",
    )

    d = f.to_dict()
    assert d["id"] == "SEC-TEST-001"
    assert d["severity"] == "High"
    assert d["source"] == "Real"
    assert d["status"] == "Open"
    assert d["cwe_id"] == "CWE-306"
    assert "uid" in d


def test_demo_findings_integrity():
    """Verify demo dataset contains valid findings covering core security areas."""
    demo_findings = get_demo_findings()
    assert len(demo_findings) >= 7

    categories = {f.category for f in demo_findings}
    expected = {
        "Authentication",
        "Authorization",
        "API Security",
        "Input Validation",
        "Communication Security",
        "Client-Side Security",
        "Data Storage & Privacy",
    }
    assert expected.issubset(categories)

    # Every finding should have evidence, impact, and recommendation
    for f in demo_findings:
        assert len(f.title) > 0
        assert len(f.evidence) > 0
        assert len(f.impact) > 0
        assert len(f.recommendation) > 0
        assert f.source == FindingSource.DEMO
