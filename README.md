# SIH26163 — World Monitor Security Assessment Platform

> **Smart India Hackathon 2026 Prototype**  
> A modular, transparent, and presentation-ready web application security assessment platform for the World Monitor application.

---

## 📌 Problem Statement: SIH26163

**Problem Title:** Security Assessment of the World Monitor Application  
**Context:** Modern infrastructure platforms like "World Monitor" aggregate telemetry, environmental metrics, and critical service data. Ensuring their confidentiality, integrity, and availability requires proactive security evaluation. SIH26163 asks participants to conduct a structured security assessment of World Monitor, detect vulnerabilities across multiple domains, assess business impact, provide actionable developer remediation, and deliver a formal executive report.

---

## 💡 Solution: Our Prototype

Instead of a simulated toy script or a generic hacker terminal, we built a **comprehensive Security Assessment Platform**:
1. **Simulated World Monitor Target App**: A self-contained, controlled local environment with realistic, testable security misconfigurations.
2. **Modular 7-Domain Assessment Engine**: Written in pure Python to perform safe, observational inspections across Authentication, Authorization, API Security, Input Validation, Transport Security, Client Cookies, and Data Privacy.
3. **Transparent Mathematical Scoring Model**: Calculates a reproducible Security Posture Score (0–100, Letter Grade A–F) with documented point deductions per severity level.
4. **Interactive Executive Dashboard**: Built with React 18, Vite, and Tailwind CSS, featuring light-mode presentation visuals, severity distribution breakdowns, and live status remediation tracking.
5. **Dynamic PDF Report Generation**: Compiles an executive-level audit report with one click using ReportLab.
6. **Ethical & Transparent**: Clear visual badges distinguishing real active scan findings from curated demonstration records.

---

## 🏛️ System Architecture

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

## ✨ Features

- **7-Domain Security Inspection**: Modular audit of Authentication, Authorization, API Headers, Input Validation, Transport Security, Client Cookies, and Data Privacy.
- **Deterministic Security Posture Score**: Base score of 100 with documented deductions:
  - Critical: `-15 pts`
  - High: `-8 pts`
  - Medium: `-4 pts`
  - Low: `-1 pt`
  - Informational: `0 pts`
- **Dynamic Score Recovery**: Marking a finding as "Fixed" instantly recovers points on the dashboard.
- **Dual Data Integrity**: Transparent distinction between **Real Scan Findings** and **Curated Demo Findings**.
- **Executive PDF Export**: Complete formal security assessment report generated on-demand with vector styling.
- **Auto-Generated REST API Docs**: Interactive Swagger UI at `http://localhost:8000/docs`.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide React |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Pydantic v2 |
| **Database** | SQLite, SQLAlchemy ORM |
| **Report Generation** | ReportLab (Vector PDF) |
| **Target App** | Flask (Simulated World Monitor) |
| **Testing** | Pytest, FastAPI TestClient, Requests |

---

## 📁 Project Structure

```text
sih26163-security-dashboard/
├── backend/                  # FastAPI Application
│   ├── routes/               # API endpoints (findings, assessment, report)
│   ├── database.py           # SQLite database connection and SQLAlchemy models
│   ├── models.py             # Pydantic schemas for request/response validation
│   ├── report_generator.py   # ReportLab PDF generation logic
│   ├── seed.py               # Database seeder for demo dataset
│   ├── main.py               # Application entrypoint & CORS configuration
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React + Vite Dashboard
│   ├── src/
│   │   ├── api/              # Axios HTTP client helper
│   │   ├── components/       # UI components (ScoreCard, Badges, Modals, Charts)
│   │   ├── pages/            # DashboardPage, FindingsPage, Methodology, About
│   │   ├── App.jsx           # Application routing & root state
│   │   └── main.jsx          # React DOM entry point
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
├── security_engine/          # Modular Security Scanner
│   ├── auth_checks.py        # Authentication & brute force checks
│   ├── authorization_checks.py # Broken access control & admin checks
│   ├── api_checks.py         # HTTP security headers & CORS policy
│   ├── input_validation_checks.py # Reflected inputs & stack trace leakage
│   ├── communication_checks.py    # HTTP vs HTTPS & plaintext credential transport
│   ├── client_security_checks.py  # Cookie flags (HttpOnly, Secure, SameSite)
│   ├── storage_checks.py     # Environment variable exposure & privacy
│   ├── finding.py            # Finding data model & scoring algorithm
│   ├── demo_data.py          # Curated representative demonstration findings
│   └── scanner.py            # Assessment orchestrator
├── target_app/               # Simulated World Monitor
│   ├── app.py                # Controlled Flask application with testable flaws
│   └── requirements.txt      # Minimal Flask dependencies
├── database/                 # SQLite database storage (assessment.db)
├── reports/                  # Generated PDF reports storage
├── docs/                     # Detailed architectural and user guides
│   ├── architecture.md
│   ├── methodology.md
│   ├── security_checks.md
│   ├── demo_guide.md
│   └── api.md
├── tests/                    # Automated unit and integration tests
│   ├── test_scoring.py
│   ├── test_engine.py
│   └── test_api.py
├── .env.example              # Environment variables template
├── .gitignore                # Production ignore configuration
└── README.md                 # Project documentation
```

---

## 🚀 Installation & Local Setup

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ and npm installed
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Ozair-aly/SIH26163.git
cd SIH26163
```

### 2. Set Up Python Virtual Environment & Backend
```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 3. Set Up React Frontend
```bash
cd frontend
npm install
cd ..
```

---

## 🏃 Running Locally

To run the complete platform for a demonstration, open three terminal windows:

### Terminal 1: Run the Simulated Target App (Port 5001)
```bash
python target_app/app.py
```
*Runs on `http://localhost:5001`.*

### Terminal 2: Run the FastAPI Backend (Port 8000)
```bash
uvicorn backend.main:app --reload --port 8000
```
*API available at `http://localhost:8000`. Swagger UI at `http://localhost:8000/docs`.*

### Terminal 3: Run the React Frontend (Port 5173)
```bash
cd frontend
npm run dev
```
*Open your browser at `http://localhost:5173`.*

---

## 🧪 Running Automated Tests

Run the full pytest suite to verify scoring models, engine functionality, and API endpoints:
```bash
pytest tests/ -v
```
*Expected: 11 passing tests in under 2 seconds.*

---

## 🔒 Security and Ethical Testing Disclaimer

- **Authorized Scope Only**: This platform is designed exclusively for educational, evaluation, and defensive security auditing within authorized environments.
- **Controlled Target**: Testing is performed strictly against the designated simulated local application (`http://localhost:5001`).
- **Non-Destructive**: All checks perform observational verification (status codes, headers, response structure) and do not conduct destructive fuzzing or denial-of-service operations.
- **No Third-Party Scanning**: Do not point the scanner at external web applications or infrastructure without explicit, written authorization.

---

## ⚠️ Prototype Limitations

1. **Static Rules Engine**: The assessment modules perform deterministic checks rather than full dynamic browser instrumentation (e.g., headless Chrome for deep DOM XSS).
2. **Educational Scoring**: The Prototype Security Score is a transparent demonstration metric, not an accredited industry rating like official CVSS v3.1 / ISO 27001.
3. **Controlled Target Scope**: Checks are targeted specifically at the patterns present in web APIs and the simulated World Monitor instance.

---

## 🔮 Future Scope

1. **AI Remediation Copilot**: Integrate an optional local LLM to generate framework-specific pull request code patches for identified findings.
2. **CI/CD Security Gate**: Package the security engine as a GitHub Action that fails pull requests if the security score drops below 75 (Grade B).
3. **SARIF / DefectDojo Export**: Support OASIS SARIF standards to export findings into enterprise vulnerability management platforms.

---

## 👥 Team Contribution (SIH 2026)

- **Problem Statement**: SIH26163 — Security Assessment of the World Monitor Application
- **Role & Scope**: Architecture design, security engine implementation, API development, React UI, testing, and documentation.
