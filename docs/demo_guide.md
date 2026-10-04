# SIH26163 Judge Presentation & Demo Guide (3–5 Minutes)

Use this step-by-step walkthrough to present the project to SIH judges.

---

## The 3–5 Minute Presentation Script

### Minute 1: Problem & Approach
> *"Good morning, respected judges. We are presenting our solution for Problem Statement **SIH26163: Security Assessment of the World Monitor Application**.*
>
> *World Monitor is a mission-critical monitoring dashboard. Our objective was not to build a toy hacker screen or make fake claims about external systems, but rather to build a **realistic, modular Security Assessment Platform** that demonstrates how enterprise security audits are conducted, scored, remediated, and reported."*

### Minute 2: The Dashboard & Security Score
1. **Show the Dashboard**:
   - Point out the **Security Scorecard** (e.g. `78/100`, Grade B/C).
   - Explain the transparent scoring model:
     > *"Rather than inventing a random score, our platform calculates this mathematically: starting at 100 points, deducting 15 for Critical, 8 for High, 4 for Medium, and 1 for Low findings."*
   - Point out the **Severity Breakdown** and the **Domain Distribution** chart showing findings across all 7 assessment categories.
   - Point out the **Source Badge**:
     > *"Judges, please note our transparency: every finding clearly states whether it was gathered from an active scan of our controlled target or loaded as part of our curated demo dataset."*

### Minute 3: Running a Live Assessment
1. Click **"Run Assessment"** in the navigation bar.
2. In the modal, explain:
   > *"Our engine targets our controlled local instance of World Monitor on port 5001. When I click 'Start Security Scan', our modular Python assessment engine inspects all seven security domains in sequence: Authentication, Authorization, API Headers, Input Validation, Transport Security, Client Cookies, and Storage Privacy."*
3. Watch the progress steps complete. The dashboard updates live with the freshly scanned findings!

### Minute 4: Deep-Dive Into a Vulnerability & Live Remediation
1. Click on **`SEC-001` (Broken Access Control — Admin Endpoint)** or **`SEC-AUTH-001` (No Rate Limiting)**.
2. The **Finding Detail Modal** opens:
   - Show the **Controlled Evidence snippet**:
     > *"Notice we document safe, non-destructive observational evidence — such as HTTP 200 returned on `/api/admin/users` without authentication."*
   - Show the **Impact Analysis** and **Developer Remediation**.
   - **Show the Live Status Update Feature**:
     - Change the status dropdown from **"Open"** to **"Fixed"**.
     - Close the modal.
     - Show the judges:
       > *"Notice that as soon as the finding is marked 'Fixed', its deduction is removed, and the application's Prototype Security Score immediately recalculated and improved!"*

### Minute 5: Report Generation & Wrap-up
1. Click **"Download Report"**.
2. A formal multi-page PDF generated dynamically by ReportLab opens:
   > *"Finally, with a single click, our platform compiles an executive-ready PDF report containing executive summary, methodology, finding matrices, proof-of-concept evidence, and remediation steps ready for developer handoff."*
3. Conclude:
   > *"Thank you, judges. We welcome any questions!"*
