"""
security_engine/finding.py
===========================
Defines the structured Finding data model.

Every security check produces one or more Finding objects.
Each finding contains all the information needed for:
  - Dashboard display
  - Detailed finding page
  - PDF report generation
  - Status tracking

This is the core data contract of the entire platform.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum
import uuid
import datetime


class Severity(str, Enum):
    """
    Severity levels following industry-standard classification.
    Maps to CVSS-inspired qualitative ratings.
    """
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"


class FindingStatus(str, Enum):
    """Lifecycle status of a finding."""
    OPEN = "Open"
    FIXED = "Fixed"
    ACCEPTED_RISK = "Accepted Risk"
    IN_PROGRESS = "In Progress"


class FindingSource(str, Enum):
    """
    Whether this finding came from a real check or is demonstration data.
    The UI MUST clearly display this distinction.
    """
    REAL = "Real"        # Finding from actual assessment of target app
    DEMO = "Demo"        # Sample finding for demonstration purposes


# ─── Severity Score Weights ───────────────────────────────────────────────────
# Used by the scoring engine to calculate the prototype security score.
# Methodology: Start at 100, subtract points per finding.
SEVERITY_DEDUCTION = {
    Severity.CRITICAL: 15,
    Severity.HIGH: 8,
    Severity.MEDIUM: 4,
    Severity.LOW: 1,
    Severity.INFORMATIONAL: 0,
}


@dataclass
class Finding:
    """
    A single security finding produced by an assessment check.

    All fields are intentionally simple strings so findings can be
    easily serialized to JSON, stored in SQLite, and displayed in the UI.
    """
    id: str                        # e.g., "SEC-001"
    title: str                     # Short human-readable title
    category: str                  # e.g., "API Security"
    severity: Severity             # Critical / High / Medium / Low / Info
    description: str               # What the issue is
    affected_component: str        # Which endpoint/component/file
    evidence: str                  # What was observed (safe, no exploits)
    impact: str                    # What could happen if exploited
    recommendation: str            # How to fix it
    source: FindingSource = FindingSource.DEMO     # Real or Demo?
    status: FindingStatus = FindingStatus.OPEN     # Current status
    cwe_id: Optional[str] = None   # Optional CWE reference (e.g., "CWE-79")
    cvss_score: Optional[float] = None  # Optional CVSS base score
    created_at: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )
    uid: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    def to_dict(self) -> dict:
        """Convert finding to a plain dictionary for JSON serialization."""
        d = asdict(self)
        d["severity"] = self.severity.value
        d["status"] = self.status.value
        d["source"] = self.source.value
        return d

    @property
    def severity_deduction(self) -> int:
        """How many points this finding deducts from the security score."""
        return SEVERITY_DEDUCTION.get(self.severity, 0)

    @property
    def severity_color(self) -> str:
        """CSS color class for UI display."""
        colors = {
            Severity.CRITICAL: "red",
            Severity.HIGH: "orange",
            Severity.MEDIUM: "yellow",
            Severity.LOW: "blue",
            Severity.INFORMATIONAL: "gray",
        }
        return colors.get(self.severity, "gray")


def calculate_security_score(findings: list[Finding]) -> dict:
    """
    Calculate the Prototype Security Score.

    Methodology (transparent, non-certified):
      - Start with a base score of 100
      - Deduct points for each finding based on severity:
          Critical: -15 points
          High:     -8  points
          Medium:   -4  points
          Low:      -1  point
          Info:      0  points
      - Minimum score is 0
      - Score applies only to Open findings

    Returns a dict with score, breakdown, and grade.
    """
    open_findings = [f for f in findings if f.status == FindingStatus.OPEN]

    total_deduction = sum(f.severity_deduction for f in open_findings)
    score = max(0, 100 - total_deduction)

    # Severity counts
    counts = {s.value: 0 for s in Severity}
    for f in open_findings:
        counts[f.severity.value] += 1

    # Grade
    if score >= 90:
        grade, grade_label = "A", "Excellent"
    elif score >= 75:
        grade, grade_label = "B", "Good"
    elif score >= 60:
        grade, grade_label = "C", "Fair"
    elif score >= 40:
        grade, grade_label = "D", "Poor"
    else:
        grade, grade_label = "F", "Critical Risk"

    return {
        "score": score,
        "base_score": 100,
        "total_deduction": total_deduction,
        "grade": grade,
        "grade_label": grade_label,
        "open_findings": len(open_findings),
        "total_findings": len(findings),
        "severity_counts": counts,
        "methodology": (
            "Prototype score: Start at 100, deduct 15 per Critical, "
            "8 per High, 4 per Medium, 1 per Low finding (Open status only). "
            "Not an industry-certified rating."
        ),
    }
