"""
tests/test_scoring.py
======================
Unit tests for the Prototype Security Scoring System.

Verifies:
  1. Base score of 100 with zero findings
  2. Accurate deductions per severity level (Critical=-15, High=-8, Medium=-4, Low=-1)
  3. Status behavior: Fixed findings do NOT deduct points
  4. Floor score constraint (score cannot drop below 0)
  5. Accurate grade assignment (A, B, C, D, F)
"""

import pytest
from security_engine.finding import (
    Finding, Severity, FindingStatus, FindingSource, calculate_security_score
)


def test_base_score_empty():
    """An application with no findings should have a score of 100 and Grade A."""
    result = calculate_security_score([])
    assert result["score"] == 100
    assert result["grade"] == "A"
    assert result["total_deduction"] == 0
    assert result["open_findings"] == 0


def test_deduction_calculation():
    """Test standard deductions for open findings."""
    findings = [
        Finding(
            id="SEC-001",
            title="Critical SQLi",
            category="Input Validation",
            severity=Severity.CRITICAL, # -15
            description="test",
            affected_component="/api",
            evidence="test",
            impact="test",
            recommendation="test",
            status=FindingStatus.OPEN,
        ),
        Finding(
            id="SEC-002",
            title="High Auth issue",
            category="Authentication",
            severity=Severity.HIGH, # -8
            description="test",
            affected_component="/api",
            evidence="test",
            impact="test",
            recommendation="test",
            status=FindingStatus.OPEN,
        ),
        Finding(
            id="SEC-003",
            title="Medium CORS",
            category="API Security",
            severity=Severity.MEDIUM, # -4
            description="test",
            affected_component="/api",
            evidence="test",
            impact="test",
            recommendation="test",
            status=FindingStatus.OPEN,
        ),
        Finding(
            id="SEC-004",
            title="Low Info",
            category="Client-Side Security",
            severity=Severity.LOW, # -1
            description="test",
            affected_component="/api",
            evidence="test",
            impact="test",
            recommendation="test",
            status=FindingStatus.OPEN,
        ),
    ]

    # Total deduction: 15 + 8 + 4 + 1 = 28
    # Score: 100 - 28 = 72 (Grade C, range 60-74)
    result = calculate_security_score(findings)
    assert result["total_deduction"] == 28
    assert result["score"] == 72
    assert result["grade"] == "C"
    assert result["open_findings"] == 4


def test_fixed_findings_do_not_deduct():
    """Remediated findings with status 'Fixed' should not reduce the score."""
    findings = [
        Finding(
            id="SEC-001",
            title="Fixed Critical",
            category="Authorization",
            severity=Severity.CRITICAL,
            description="test",
            affected_component="/api",
            evidence="test",
            impact="test",
            recommendation="test",
            status=FindingStatus.FIXED, # Fixed! No deduction
        ),
        Finding(
            id="SEC-002",
            title="Open Low",
            category="Communication Security",
            severity=Severity.LOW,
            description="test",
            affected_component="/api",
            evidence="test",
            impact="test",
            recommendation="test",
            status=FindingStatus.OPEN, # -1
        ),
    ]

    result = calculate_security_score(findings)
    assert result["total_deduction"] == 1
    assert result["score"] == 99
    assert result["grade"] == "A"
    assert result["open_findings"] == 1
    assert result["total_findings"] == 2


def test_score_floor_zero():
    """Score should not fall below 0 even with catastrophic deductions."""
    many_criticals = [
        Finding(
            id=f"SEC-{i}",
            title="Critical",
            category="Auth",
            severity=Severity.CRITICAL,
            description="test",
            affected_component="/api",
            evidence="test",
            impact="test",
            recommendation="test",
            status=FindingStatus.OPEN,
        )
        for i in range(10) # 10 * 15 = 150 points deduction
    ]

    result = calculate_security_score(many_criticals)
    assert result["score"] == 0
    assert result["grade"] == "F"
