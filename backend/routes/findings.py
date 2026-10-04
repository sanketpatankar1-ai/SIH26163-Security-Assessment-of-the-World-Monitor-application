"""
backend/routes/findings.py
===========================
Findings API Routes

Endpoints:
  GET  /api/findings          — List all findings (with optional filters)
  GET  /api/findings/{uid}    — Get a single finding by UID
  PATCH /api/findings/{uid}   — Update finding status

These endpoints serve the findings list page and detail page in the frontend.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.database import get_db, FindingModel
from backend.models import FindingResponse, FindingStatusUpdate

router = APIRouter(prefix="/api/findings", tags=["Findings"])


@router.get("", response_model=List[FindingResponse])
def list_findings(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    source: Optional[str] = Query(None, description="Filter by source (Real/Demo)"),
    db: Session = Depends(get_db),
):
    """
    List all findings with optional filtering.

    Query parameters allow the frontend to filter by severity, category, status, or source.
    Example: GET /api/findings?severity=High&status=Open
    """
    query = db.query(FindingModel)

    if severity:
        query = query.filter(FindingModel.severity == severity)
    if category:
        query = query.filter(FindingModel.category == category)
    if status:
        query = query.filter(FindingModel.status == status)
    if source:
        query = query.filter(FindingModel.source == source)

    raw_findings = query.order_by(FindingModel.id).all()
    unique_dict = {}
    for f in raw_findings:
        if f.id not in unique_dict:
            unique_dict[f.id] = f
        elif f.status in ["Fixed", "Accepted Risk", "In Progress"]:
            unique_dict[f.id] = f
    return list(unique_dict.values())


@router.get("/{uid}", response_model=FindingResponse)
def get_finding(uid: str, db: Session = Depends(get_db)):
    """
    Get a single finding by its unique ID (UUID).
    Used by the finding detail page.
    """
    finding = db.query(FindingModel).filter(FindingModel.uid == uid).first()
    if not finding:
        raise HTTPException(status_code=404, detail=f"Finding '{uid}' not found")
    return finding


@router.patch("/{uid}", response_model=FindingResponse)
def update_finding_status(
    uid: str,
    update: FindingStatusUpdate,
    db: Session = Depends(get_db),
):
    """
    Update the status of a finding.

    Allowed status values: Open, Fixed, Accepted Risk, In Progress

    This allows the security team to track remediation progress
    directly in the dashboard.
    """
    finding = db.query(FindingModel).filter(FindingModel.uid == uid).first()
    if not finding:
        raise HTTPException(status_code=404, detail=f"Finding '{uid}' not found")

    finding.status = update.status.value
    db.commit()
    db.refresh(finding)
    return finding
