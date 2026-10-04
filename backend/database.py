"""
backend/database.py
====================
SQLite Database Setup using SQLAlchemy

Tables:
  - assessments     : Each assessment run record
  - findings        : All findings from assessments
  - assessment_runs : Log of when assessments were triggered

SQLAlchemy handles:
  - Database creation (auto)
  - Table creation (auto on startup)
  - Session management
"""

from sqlalchemy import (
    create_engine, Column, String, Integer, Float,
    Text, DateTime, Boolean, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import os

# ─── Database path ────────────────────────────────────────────────────────────
# Creates database/ folder if it doesn't exist
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
os.makedirs(DB_DIR, exist_ok=True)
DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'assessment.db')}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite with FastAPI
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ─── Database Models ──────────────────────────────────────────────────────────

class AssessmentModel(Base):
    """Represents a full assessment run."""
    __tablename__ = "assessments"

    id = Column(String, primary_key=True)          # e.g., ASSESS-20240917-143022
    target_url = Column(String, nullable=False)
    started_at = Column(String, nullable=False)
    completed_at = Column(String, nullable=True)
    status = Column(String, default="pending")     # pending | completed | failed
    score = Column(Integer, nullable=True)
    grade = Column(String, nullable=True)
    total_findings = Column(Integer, default=0)
    disclaimer = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    findings = relationship("FindingModel", back_populates="assessment")


class FindingModel(Base):
    """Represents a single security finding."""
    __tablename__ = "findings"

    uid = Column(String, primary_key=True)         # UUID
    id = Column(String, nullable=False)            # e.g., SEC-001
    assessment_id = Column(String, ForeignKey("assessments.id"), nullable=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)      # Critical | High | Medium | Low | Informational
    description = Column(Text, nullable=False)
    affected_component = Column(String, nullable=False)
    evidence = Column(Text, nullable=False)
    impact = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    source = Column(String, default="Demo")        # Real | Demo
    status = Column(String, default="Open")        # Open | Fixed | Accepted Risk | In Progress
    cwe_id = Column(String, nullable=True)
    cvss_score = Column(Float, nullable=True)
    created_at = Column(String, nullable=True)
    is_demo = Column(Boolean, default=True)

    assessment = relationship("AssessmentModel", back_populates="findings")


# ─── Utility functions ────────────────────────────────────────────────────────

def get_db():
    """FastAPI dependency — yields a database session and closes it after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Called once on application startup."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")
