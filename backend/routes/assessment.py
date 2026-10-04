"""
backend/routes/assessment.py
==============================
Assessment API Routes

Endpoints:
  GET  /api/dashboard          — Dashboard summary data
  POST /api/assessment/run     — Trigger a new assessment
  GET  /api/assessment/history — List past assessments
"""

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from collections import Counter
import sys, os, uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.database import get_db, FindingModel, AssessmentModel
from backend.models import (
    AssessmentRunRequest, DashboardResponse, FindingResponse, HealthResponse
)

router = APIRouter(tags=["Assessment"])


@router.get("/api/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Simple health check endpoint. Verifies database connectivity."""
    try:
        db.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "version": "1.0.0",
        "database": db_status,
        "demo_mode": True,
    }


@router.get("/api/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    """
    Returns aggregated data for the main dashboard.

    Calculates:
    - Security score (based on active unique open findings)
    - Severity distribution
    - Category distribution
    - Recent findings (last 5)
    - Last assessment timestamp
    """
    from security_engine.finding import calculate_security_score, Finding, Severity, FindingStatus, FindingSource

    all_findings_db = db.query(FindingModel).all()

    # Deduplicate findings by finding ID to prevent accumulation across repeated runs
    unique_dict = {}
    for f in all_findings_db:
        if f.id not in unique_dict:
            unique_dict[f.id] = f
        else:
            # Preserve user modifications (e.g. Fixed or Accepted Risk)
            if f.status in ["Fixed", "Accepted Risk", "In Progress"]:
                unique_dict[f.id] = f

    findings_db = list(unique_dict.values())

    # Convert DB rows back to Finding objects for scoring
    findings = []
    for f in findings_db:
        try:
            finding = Finding(
                id=f.id,
                title=f.title,
                category=f.category,
                severity=Severity(f.severity),
                description=f.description,
                affected_component=f.affected_component,
                evidence=f.evidence,
                impact=f.impact,
                recommendation=f.recommendation,
                source=FindingSource(f.source),
                status=FindingStatus(f.status),
                cwe_id=f.cwe_id,
                cvss_score=f.cvss_score,
                uid=f.uid,
            )
            findings.append(finding)
        except Exception:
            pass

    score_data = calculate_security_score(findings)

    # Category distribution
    category_counts = Counter(f.category for f in findings_db)

    # Last assessment
    last = db.query(AssessmentModel).order_by(AssessmentModel.created_at.desc()).first()

    # Recent findings (last 5, sorted by severity)
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}
    sorted_findings = sorted(findings_db, key=lambda f: severity_order.get(f.severity, 5))[:5]

    return DashboardResponse(
        security_score=score_data["score"],
        grade=score_data["grade"],
        grade_label=score_data["grade_label"],
        total_findings=score_data["total_findings"],
        open_findings=score_data["open_findings"],
        severity_counts=score_data["severity_counts"],
        category_counts=dict(category_counts),
        recent_findings=sorted_findings,
        last_assessment=last.completed_at if last else None,
        methodology=score_data["methodology"],
        disclaimer=(
            "Prototype Security Score — Not an industry-certified rating. "
            "Assessment performed on a controlled simulated target."
        ),
    )


@router.post("/api/assessment/run")
def run_assessment(
    request: AssessmentRunRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Trigger a new security assessment.

    Runs all check modules against the target URL,
    upserts findings in the database to prevent duplicate accumulation,
    and updates the security score.
    """
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from security_engine.scanner import run_assessment as engine_run

    result = engine_run(
        target_url=request.target_url,
        include_demo=request.include_demo,
    )

    # Save assessment record
    assessment = AssessmentModel(
        id=result["assessment_id"],
        target_url=result["target_url"],
        started_at=result["started_at"],
        completed_at=result["completed_at"],
        status=result["status"],
        score=result["score"]["score"],
        grade=result["score"]["grade"],
        total_findings=len(result["findings"]),
        disclaimer=result["disclaimer"],
    )
    db.add(assessment)

    # Upsert findings by rule ID
    for f_data in result["findings"]:
        existing = db.query(FindingModel).filter(FindingModel.id == f_data["id"]).first()
        if existing:
            existing.title = f_data["title"]
            existing.category = f_data["category"]
            existing.severity = f_data["severity"]
            existing.description = f_data["description"]
            existing.affected_component = f_data["affected_component"]
            existing.evidence = f_data["evidence"]
            existing.impact = f_data["impact"]
            existing.recommendation = f_data["recommendation"]
            existing.source = f_data["source"]
            existing.assessment_id = result["assessment_id"]
            if existing.status not in ["Fixed", "Accepted Risk"]:
                existing.status = f_data["status"]
        else:
            finding = FindingModel(
                uid=f_data["uid"],
                id=f_data["id"],
                assessment_id=result["assessment_id"],
                title=f_data["title"],
                category=f_data["category"],
                severity=f_data["severity"],
                description=f_data["description"],
                affected_component=f_data["affected_component"],
                evidence=f_data["evidence"],
                impact=f_data["impact"],
                recommendation=f_data["recommendation"],
                source=f_data["source"],
                status=f_data["status"],
                cwe_id=f_data.get("cwe_id"),
                cvss_score=f_data.get("cvss_score"),
                created_at=f_data.get("created_at"),
                is_demo=(f_data["source"] == "Demo"),
            )
            db.add(finding)

    db.commit()

    return {
        "message": "Assessment completed",
        "assessment_id": result["assessment_id"],
        "findings_count": len(result["findings"]),
        "score": result["score"]["score"],
        "grade": result["score"]["grade"],
    }


@router.post("/api/assessment/reset")
def reset_assessment(db: Session = Depends(get_db)):
    """
    Resets the database back to the clean baseline demo dataset.
    Useful for demonstration resets.
    """
    db.query(FindingModel).delete()
    db.query(AssessmentModel).delete()
    db.commit()

    from backend.seed import seed_database
    seed_database()

    return {"message": "Database successfully reset to baseline demo dataset"}


@router.get("/api/assessment/history")
def assessment_history(db: Session = Depends(get_db)):
    """Return list of past assessment runs."""
    assessments = db.query(AssessmentModel).order_by(
        AssessmentModel.created_at.desc()
    ).limit(10).all()

    return [
        {
            "id": a.id,
            "target_url": a.target_url,
            "started_at": a.started_at,
            "completed_at": a.completed_at,
            "score": a.score,
            "grade": a.grade,
            "total_findings": a.total_findings,
            "status": a.status,
        }
        for a in assessments
    ]
