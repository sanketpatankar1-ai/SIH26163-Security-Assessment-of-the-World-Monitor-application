"""
security_engine/authorization_checks.py
=========================================
Authorization & Access Control Checks

What we check:
  - Are admin endpoints protected?
  - Can unauthenticated users access protected resources?
  - Is there proper role enforcement?

Method: Send unauthenticated requests to endpoints that should require auth.
Observe whether access is granted or denied. No exploitation — just observation.
"""

import requests
from .finding import Finding, Severity, FindingSource


def run_authorization_checks(target_url: str) -> list[Finding]:
    """Run all authorization checks."""
    findings = []
    findings.extend(_check_unauth_data_access(target_url))
    findings.extend(_check_admin_endpoint_exposure(target_url))
    findings.extend(_check_debug_endpoint(target_url))
    return findings


def _check_unauth_data_access(target_url: str) -> list[Finding]:
    """
    Check if protected data endpoints require authentication.
    A properly secured API should return 401 or 403 without valid credentials.
    """
    findings = []
    protected_url = f"{target_url}/api/data"

    try:
        # Request without any auth headers or session cookies
        r = requests.get(protected_url, timeout=5)

        if r.status_code == 200:
            findings.append(Finding(
                id="SEC-AUTHZ-001",
                title="Unauthenticated Access to Protected Data Endpoint",
                category="Authorization",
                severity=Severity.HIGH,
                description=(
                    "The /api/data endpoint returns monitoring data without "
                    "requiring authentication. Any unauthenticated user or script "
                    "can access sensitive operational data."
                ),
                affected_component="/api/data",
                evidence=(
                    f"GET {protected_url} (no auth headers, no session cookie) "
                    f"returned HTTP 200 with data payload. "
                    f"Response contained {len(r.json().get('data', []))} records."
                ),
                impact=(
                    "Sensitive World Monitor data (sensor readings, locations, status) "
                    "is accessible to anyone who discovers the API endpoint, without login."
                ),
                recommendation=(
                    "1. Add authentication check to every protected endpoint.\n"
                    "2. Return HTTP 401 (Unauthorized) if no valid token/session.\n"
                    "3. Use a decorator pattern:\n"
                    "   @login_required (Flask-Login) or\n"
                    "   Depends(get_current_user) (FastAPI)\n"
                    "4. Apply principle of least privilege — only return data the user's role permits."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-862",
            ))

    except requests.RequestException:
        pass

    return findings


def _check_admin_endpoint_exposure(target_url: str) -> list[Finding]:
    """
    Check if admin-only endpoints are accessible without admin role.
    """
    findings = []
    admin_url = f"{target_url}/api/admin/users"

    try:
        r = requests.get(admin_url, timeout=5)

        if r.status_code == 200:
            findings.append(Finding(
                id="SEC-AUTHZ-002",
                title="Admin Endpoint Accessible Without Authorization",
                category="Authorization",
                severity=Severity.CRITICAL,
                description=(
                    "The /api/admin/users endpoint — which should be restricted to "
                    "administrator accounts — is accessible to unauthenticated requests. "
                    "This is a Broken Access Control vulnerability (OWASP Top 10 #1)."
                ),
                affected_component="/api/admin/users",
                evidence=(
                    f"GET {admin_url} (no auth) returned HTTP 200. "
                    f"Response disclosed user list: {r.text[:200]}"
                ),
                impact=(
                    "An attacker can enumerate all user accounts in the system "
                    "without authentication, enabling targeted attacks against specific accounts."
                ),
                recommendation=(
                    "1. Enforce role-based access control (RBAC).\n"
                    "2. Check session role before serving admin endpoints:\n"
                    "   if session.get('role') != 'admin': abort(403)\n"
                    "3. Return HTTP 403 (Forbidden) for unauthorized access.\n"
                    "4. Log all unauthorized access attempts."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-285",
                cvss_score=9.1,
            ))

    except requests.RequestException:
        pass

    return findings


def _check_debug_endpoint(target_url: str) -> list[Finding]:
    """Check if a debug endpoint is exposed that leaks internal information."""
    findings = []
    debug_url = f"{target_url}/debug"

    try:
        r = requests.get(debug_url, timeout=5)

        if r.status_code == 200:
            data = r.json()
            has_env = "env_vars" in data

            findings.append(Finding(
                id="SEC-AUTHZ-003",
                title="Debug Endpoint Exposed — Environment Variable Leakage",
                category="Authorization",
                severity=Severity.HIGH,
                description=(
                    "A /debug endpoint is publicly accessible and returns internal "
                    "application configuration including all environment variables. "
                    "Environment variables often contain database passwords, API keys, "
                    "and other secrets."
                ),
                affected_component="/debug",
                evidence=(
                    f"GET {debug_url} returned HTTP 200. "
                    f"Response includes environment variables: {has_env}. "
                    "Config keys exposed: " + str(list(data.get("config", {}).keys()))
                ),
                impact=(
                    "Exposure of environment variables can reveal database credentials, "
                    "secret keys, cloud provider tokens, and internal infrastructure details "
                    "— effectively granting an attacker full system access."
                ),
                recommendation=(
                    "1. Remove all debug/diagnostic endpoints before deployment.\n"
                    "2. If needed internally, protect with IP allowlist or admin auth.\n"
                    "3. Set DEBUG=False in production configuration.\n"
                    "4. Use a secrets manager (not env vars) for sensitive credentials."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-215",
            ))

    except requests.RequestException:
        pass

    return findings
