"""
backend/seed.py
================
Database Seeder

Loads the demo dataset into the database so the dashboard
is populated immediately when the app is first opened.

Run once: python backend/seed.py

Or it's called automatically from main.py on startup
if the database is empty.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.database import SessionLocal, init_db, FindingModel, AssessmentModel
from security_engine.demo_data import get_demo_findings
from security_engine.finding import calculate_security_score, Finding, Severity, FindingStatus, FindingSource
import datetime


def seed_database():
    """Seed the database with demo findings if empty."""
    init_db()
    db = SessionLocal()

    try:
        existing = db.query(FindingModel).count()
        if existing > 0:
            print(f"Database already has {existing} findings. Skipping seed.")
            return

        print("Seeding database with demo findings...")

        # Create a demo assessment record
        demo_assessment = AssessmentModel(
            id="ASSESS-DEMO-001",
            target_url="http://localhost:5001 (Simulated World Monitor)",
            started_at=datetime.datetime.utcnow().isoformat(),
            completed_at=datetime.datetime.utcnow().isoformat(),
            status="completed",
            score=0,  # Will update after calculating
            grade="",
            total_findings=0,
            disclaimer=(
                "DEMO DATA — This assessment used sample findings for demonstration. "
                "Not a real production assessment."
            ),
        )
        db.add(demo_assessment)

        # Load and save demo findings
        demo_findings = get_demo_findings()

        # Calculate score
        finding_objects = []
        for f_data in demo_findings:
            finding_objects.append(Finding(
                id=f_data.id,
                title=f_data.title,
                category=f_data.category,
                severity=Severity(f_data.severity.value),
                description=f_data.description,
                affected_component=f_data.affected_component,
                evidence=f_data.evidence,
                impact=f_data.impact,
                recommendation=f_data.recommendation,
                source=FindingSource(f_data.source.value),
                status=FindingStatus(f_data.status.value),
                cwe_id=f_data.cwe_id,
                cvss_score=f_data.cvss_score,
                uid=f_data.uid,
            ))

        score_data = calculate_security_score(finding_objects)
        demo_assessment.score = score_data["score"]
        demo_assessment.grade = score_data["grade"]
        demo_assessment.total_findings = len(demo_findings)

        for f in demo_findings:
            db_finding = FindingModel(
                uid=f.uid,
                id=f.id,
                assessment_id="ASSESS-DEMO-001",
                title=f.title,
                category=f.category,
                severity=f.severity.value,
                description=f.description,
                affected_component=f.affected_component,
                evidence=f.evidence,
                impact=f.impact,
                recommendation=f.recommendation,
                source=f.source.value,
                status=f.status.value,
                cwe_id=f.cwe_id,
                cvss_score=f.cvss_score,
                created_at=f.created_at,
                is_demo=True,
            )
            db.add(db_finding)

        db.commit()
        print(f"Seeded {len(demo_findings)} demo findings.")
        print(f"Demo Security Score: {score_data['score']}/100 ({score_data['grade']})")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
