"""
backend/routes/report.py
==========================
Report Generation Route

GET /api/report  — Generate a PDF security assessment report

Uses ReportLab to create a professional PDF containing:
  - Executive Summary
  - Assessment Scope
  - Methodology
  - Security Overview (score, grade)
  - All Findings with evidence and recommendations
  - Limitations
  - Conclusion
"""

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os, datetime

from backend.database import get_db, FindingModel, AssessmentModel
from backend.report_generator import generate_pdf_report

router = APIRouter(tags=["Report"])


@router.get("/api/report")
def generate_report(db: Session = Depends(get_db)):
    """
    Generate a PDF security assessment report and return it as a download.
    """
    findings = db.query(FindingModel).order_by(FindingModel.id).all()
    last_assessment = db.query(AssessmentModel).order_by(
        AssessmentModel.created_at.desc()
    ).first()

    # Generate the PDF
    report_path = generate_pdf_report(findings, last_assessment)

    return FileResponse(
        path=report_path,
        media_type="application/pdf",
        filename=f"world-monitor-security-report-{datetime.date.today()}.pdf",
    )
