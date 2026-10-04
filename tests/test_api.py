"""
tests/test_api.py
==================
Integration tests for FastAPI endpoints.

Verifies:
  1. GET /api/health
  2. GET /api/dashboard
  3. GET /api/findings
  4. PATCH /api/findings/{uid}
  5. GET /api/report (PDF generation)
"""

import pytest
from fastapi.testclient import TestClient
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.main import app
from backend.seed import seed_database

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_database()


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"


def test_dashboard_endpoint():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "security_score" in data
    assert "severity_counts" in data
    assert "category_counts" in data
    assert "recent_findings" in data
    assert 0 <= data["security_score"] <= 100


def test_findings_list_endpoint():
    response = client.get("/api/findings")
    assert response.status_code == 200
    findings = response.json()
    assert isinstance(findings, list)
    assert len(findings) > 0


def test_finding_patch_status():
    # First fetch list to get a valid UID
    res = client.get("/api/findings")
    findings = res.json()
    assert len(findings) > 0

    target = findings[0]
    uid = target["uid"]

    # Patch to "Fixed"
    patch_res = client.patch(f"/api/findings/{uid}", json={"status": "Fixed"})
    assert patch_res.status_code == 200
    updated = patch_res.json()
    assert updated["status"] == "Fixed"

    # Revert back to "Open"
    revert_res = client.patch(f"/api/findings/{uid}", json={"status": "Open"})
    assert revert_res.status_code == 200
    assert revert_res.json()["status"] == "Open"


def test_report_pdf_endpoint():
    response = client.get("/api/report")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000 # Valid non-empty PDF
