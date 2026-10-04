# System Architecture — SIH26163 Security Assessment Platform

## 1. Overview

The **World Monitor Security Assessment Platform** is built as an end-to-end prototype for Smart India Hackathon 2026. It is designed to illustrate how an enterprise security team audits a web application, maps observational evidence into structured vulnerability findings, computes a deterministic security posture score, tracks developer remediation, and generates auditable PDF reports.

---

## 2. Architecture Diagram

```text
+-------------------------------------------------------------------------+
|                  Presentation Layer: React 18 + Vite                    |
|-------------------------------------------------------------------------|
|  - Executive Dashboard (KPIs, Scorecard, Category Breakdown)            |
|  - Findings Repository (Search, Filter by Severity / Source / Status)   |
|  - Detailed Finding Inspection (Evidence, PoC, Impact, Remediation)     |
|  - Live Status Updating (Open -> In Progress -> Fixed -> Score Updates) |
|  - One-click PDF Export Trigger                                         |
+-------------------------------------------------------------------------+
                                    |
                             HTTP / REST (JSON)
                                    v
+-------------------------------------------------------------------------+
|                    Application Layer: FastAPI (Python)                  |
|-------------------------------------------------------------------------|
|  - Router: /api/dashboard          (Metrics, Aggregations)              |
|  - Router: /api/findings           (CRUD, Status Patching)              |
|  - Router: /api/assessment/run     (Engine Trigger)                     |
|  - Router: /api/report             (PDF Generation via ReportLab)       |
|  - Pydantic Schema Validation      (Data Contracts)                     |
+-------------------------------------------------------------------------+
            |                                         |
            v                                         v
+-----------------------+                 +-------------------------------+
|     SQLite Database   |                 |    Security Assessment Engine |
|-----------------------|                 |-------------------------------|
| - assessments table   |                 | - scanner.py (Orchestrator)   |
| - findings table      |                 | - finding.py (Data Contract)  |
| - SQLAlchemy ORM      |                 | - 7 Assessment Domain Modules |
+-----------------------+                 +-------------------------------+
                                                          |
                                               Safe HTTP Inspection
                                                          v
                                          +-------------------------------+
                                          |   Simulated Target App        |
                                          |   (World Monitor - Port 5001) |
                                          |-------------------------------|
                                          | - Weak Auth & Admin Routes    |
                                          | - Missing HTTP Headers        |
                                          | - Diagnostic Endpoints        |
                                          +-------------------------------+
```

---

## 3. Technology Stack & Rationale

| Component | Selected Technology | Technical Justification |
|---|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS | Lightning-fast HMR, component-driven UI, zero-bloat styling, modern clean aesthetic. |
| **Icons & Charts** | Lucide React, SVG Charts | Crisp, lightweight icons and responsive data visualizations. |
| **Backend** | Python FastAPI | High-performance asynchronous REST API, native Pydantic validation, auto-generated Swagger UI at `/docs`. |
| **Database** | SQLite + SQLAlchemy ORM | Zero configuration, self-contained serverless storage, perfect for demo portable environments. |
| **Report Engine** | ReportLab | Programmatic, multi-page vector PDF generation with custom headers, tables, and pagination. |
| **Assessment Engine** | Python `requests` & urllib | Pure Python modules without heavy external scanner binaries, ensuring reproducible execution on any machine. |
| **Target App** | Python Flask | Minimal simulated World Monitor service containing intentionally testable security configurations. |

---

## 4. Component Separation & Flow

1. **Target App (`target_app/`)**: Runs independently on port 5001. Represents the controlled target surface.
2. **Security Engine (`security_engine/`)**: Contains pure audit modules. Makes observational HTTP calls to port 5001 and yields structured `Finding` objects.
3. **Backend API (`backend/`)**: Exposes REST endpoints, persists findings to `database/assessment.db`, and exposes `/docs` and `/api/report`.
4. **Frontend Client (`frontend/`)**: Communicates with the backend over port 8000. Provides real-time status updates and filtering.
