# API Documentation — World Monitor Security Assessment Platform

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

---

## Base URL
`http://localhost:8000`

---

## Endpoints

### 1. Health & Status
#### `GET /api/health`
Returns system health and database connection status.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": "connected",
  "demo_mode": true
}
```

---

### 2. Dashboard Metrics
#### `GET /api/dashboard`
Returns aggregated metrics for the dashboard view, including the calculated security score, grade, severity breakdown, category breakdown, and recent findings.

**Response:**
```json
{
  "security_score": 78,
  "grade": "B",
  "grade_label": "Good",
  "total_findings": 8,
  "open_findings": 7,
  "severity_counts": {
    "Critical": 2,
    "High": 2,
    "Medium": 3,
    "Low": 1,
    "Informational": 0
  },
  "category_counts": {
    "Authentication": 2,
    "Authorization": 1,
    "API Security": 1
  },
  "recent_findings": [...],
  "last_assessment": "2026-09-17T07:45:00Z",
  "methodology": "Prototype score: Start at 100, deduct 15 per Critical...",
  "disclaimer": "Prototype Security Score — Not an industry-certified rating."
}
```

---

### 3. Findings Management
#### `GET /api/findings`
Lists findings with optional query filtering.

**Query Parameters:**
- `severity` (string, optional): Filter by Critical, High, Medium, Low, Informational
- `category` (string, optional): Filter by domain (e.g. Authentication, Authorization)
- `status` (string, optional): Filter by Open, In Progress, Fixed, Accepted Risk
- `source` (string, optional): Filter by Real or Demo

#### `GET /api/findings/{uid}`
Retrieves complete details for a single finding.

#### `PATCH /api/findings/{uid}`
Updates a finding's remediation lifecycle status.

**Request Body:**
```json
{
  "status": "Fixed"
}
```

---

### 4. Assessment Execution
#### `POST /api/assessment/run`
Triggers an automated scan against the specified target.

**Request Body:**
```json
{
  "target_url": "http://localhost:5001",
  "include_demo": false
}
```

**Response:**
```json
{
  "message": "Assessment completed",
  "assessment_id": "ASSESS-20260917-074500",
  "findings_count": 8,
  "score": 78,
  "grade": "B"
}
```

---

### 5. Report Export
#### `GET /api/report`
Dynamically renders and streams an executive-ready multi-page PDF assessment report.

**Response Header:** `Content-Type: application/pdf`
