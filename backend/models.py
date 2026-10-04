"""
backend/models.py
==================
Pydantic Models for API Request/Response Validation

Pydantic models serve two purposes:
  1. Input validation — reject bad requests automatically
  2. Response serialization — control exactly what gets sent to the frontend

These are separate from SQLAlchemy models (database.py).
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class SeverityEnum(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"


class StatusEnum(str, Enum):
    OPEN = "Open"
    FIXED = "Fixed"
    ACCEPTED_RISK = "Accepted Risk"
    IN_PROGRESS = "In Progress"


class SourceEnum(str, Enum):
    REAL = "Real"
    DEMO = "Demo"


# ─── Finding Schemas ──────────────────────────────────────────────────────────

class FindingResponse(BaseModel):
    """Response model for a single finding."""
    uid: str
    id: str
    title: str
    category: str
    severity: str
    description: str
    affected_component: str
    evidence: str
    impact: str
    recommendation: str
    source: str
    status: str
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    created_at: Optional[str] = None
    assessment_id: Optional[str] = None

    class Config:
        from_attributes = True


class FindingStatusUpdate(BaseModel):
    """Request body for updating a finding's status."""
    status: StatusEnum = Field(..., description="New status for the finding")


# ─── Assessment Schemas ───────────────────────────────────────────────────────

class AssessmentRunRequest(BaseModel):
    """Request to trigger a new assessment."""
    target_url: str = Field(
        default="http://localhost:5001",
        description="URL of the application to assess"
    )
    include_demo: bool = Field(
        default=False,
        description="Include demo/sample findings alongside real findings"
    )


class SeverityCounts(BaseModel):
    Critical: int = 0
    High: int = 0
    Medium: int = 0
    Low: int = 0
    Informational: int = 0


class ScoreData(BaseModel):
    score: int
    base_score: int
    total_deduction: int
    grade: str
    grade_label: str
    open_findings: int
    total_findings: int
    severity_counts: dict
    methodology: str


class AssessmentResponse(BaseModel):
    """Response model for a completed assessment."""
    assessment_id: str
    target_url: str
    started_at: str
    completed_at: Optional[str]
    status: str
    findings: List[FindingResponse]
    score: ScoreData
    disclaimer: str

    class Config:
        from_attributes = True


# ─── Dashboard Schema ─────────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    """Aggregated data for the dashboard overview."""
    security_score: int
    grade: str
    grade_label: str
    total_findings: int
    open_findings: int
    severity_counts: dict
    category_counts: dict
    recent_findings: List[FindingResponse]
    last_assessment: Optional[str]
    methodology: str
    disclaimer: str


# ─── Health Check ─────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    demo_mode: bool
