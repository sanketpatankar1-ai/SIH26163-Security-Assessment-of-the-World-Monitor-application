# Security Assessment Methodology & Scoring Guide

## 1. Overview

This document describes the security assessment methodology implemented in the SIH26163 platform. The goal is to provide judges and technical evaluators with a clear, transparent framework explaining how risks are detected, categorized, and scored.

---

## 2. Prototype Security Scoring Model

Unlike closed-source commercial scanners that output opaque, proprietary vulnerability scores, our prototype implements a **fully transparent, mathematical scoring formula**.

### Formula

$$\text{Score} = \max\left(0, 100 - \sum_{i} \left( \text{Count}(\text{Open Findings at Severity}_i) \times \text{Deduction}_i \right)\right)$$

### Severity Weights Table

| Qualitative Severity | Point Deduction per Finding | Criteria |
|---|---|---|
| **Critical** | **-15 points** | Immediate administrative compromise, unauthenticated remote control, or complete credential exposure. |
| **High** | **-8 points** | Broken access control to sensitive endpoints, lack of authentication on protected datasets, plaintext credential transport. |
| **Medium** | **-4 points** | Missing defense-in-depth controls, lack of security headers, reflected input indicators, permissive CORS. |
| **Low** | **-1 point** | Non-sensitive information disclosure, missing transport hardening directives (HSTS). |
| **Informational** | **0 points** | Technical fingerprinting, server banners, informational configuration observations. |

### Letter Grade Scale

- **90 – 100**: Grade **A** (Excellent Posture)
- **75 – 89**: Grade **B** (Good Posture, minor hardening recommended)
- **60 – 74**: Grade **C** (Fair Posture, moderate risk items active)
- **40 – 59**: Grade **D** (Poor Posture, significant exposure present)
- **0 – 39**: Grade **F** (Critical Risk, urgent remediation mandatory)

### Dynamic Score Recovery Feature

A key feature demonstrated for SIH judges is **remediation reactivity**:
When a security analyst or developer reviews a finding and marks its status as **"Fixed"**, that finding is removed from the active penalty deduction list. The application's score immediately recalculates and recovers in real time.

---

## 3. The 7 Assessment Domains

1. **Authentication & Session Management**: Evaluates rate-limiting resilience, default credential resistance, and session token randomness.
2. **Authorization & Access Control**: Verifies role-based access control (RBAC), detects Broken Access Control (OWASP Top 10 #1), and checks for unauthorized diagnostic exposure.
3. **API Security**: Scans for mandatory HTTP security headers (X-Frame-Options, CSP, X-Content-Type-Options) and detects permissive CORS wildcards (`*`).
4. **Input Validation**: Evaluates parameter reflection without output encoding (XSS precursor) and detects verbose debug stack trace disclosure.
5. **Communication Security**: Checks for unencrypted HTTP transport, verifies whether sensitive credentials are transmitted in plaintext, and inspects HSTS headers.
6. **Client-Side Security**: Analyzes Set-Cookie security directives (`HttpOnly`, `Secure`, `SameSite`) to protect against token exfiltration.
7. **Data Storage & Privacy**: Detects server environment variable disclosure, exposed debug endpoints, and non-essential sensitive field exposure.

---

## 4. Ethical Security Testing Protocol

1. **Authorized Scope Only**: Testing is strictly limited to the locally hosted or designated simulated World Monitor container (`http://localhost:5001`).
2. **Non-Destructive Observation**: The assessment engine uses observational checks (inspecting HTTP response codes, response bodies, and header configurations) rather than destructive fuzzing.
3. **No External Scanning**: The engine refuses to scan third-party or unauthorized external domains.
