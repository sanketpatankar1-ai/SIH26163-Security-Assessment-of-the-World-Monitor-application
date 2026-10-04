# security_engine/__init__.py
# Makes security_engine a Python package
from .finding import Finding, Severity, FindingStatus, FindingSource, calculate_security_score
from .scanner import run_assessment
from .demo_data import get_demo_findings

__all__ = [
    "Finding",
    "Severity",
    "FindingStatus",
    "FindingSource",
    "calculate_security_score",
    "run_assessment",
    "get_demo_findings",
]
