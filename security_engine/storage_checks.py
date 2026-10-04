"""
security_engine/storage_checks.py
=====================================
Data Storage & Privacy Checks

What we check:
  - Sensitive data in API responses that shouldn't be there
  - Debug endpoint data leakage (env vars)
  - Unnecessary data retention patterns
"""

import requests
from .finding import Finding, Severity, FindingSource


def run_storage_checks(target_url: str) -> list[Finding]:
    """Run data storage and privacy checks."""
    findings = []
    findings.extend(_check_env_var_exposure(target_url))
    findings.extend(_check_response_data_minimization(target_url))
    return findings


def _check_env_var_exposure(target_url: str) -> list[Finding]:
    """
    Check if environment variables are accessible via any endpoint.
    Env vars often contain database passwords, API keys, cloud credentials.
    """
    findings = []

    try:
        r = requests.get(f"{target_url}/debug", timeout=5)

        if r.status_code == 200:
            data = r.json()
            env_count = len(data.get("env_vars", {}))

            if env_count > 0:
                findings.append(Finding(
                    id="SEC-STORE-001",
                    title="Environment Variables Exposed via Debug Endpoint",
                    category="Data Storage & Privacy",
                    severity=Severity.CRITICAL,
                    description=(
                        "The /debug endpoint exposes all server environment variables "
                        "in the HTTP response. Environment variables frequently contain "
                        "database passwords, cloud provider credentials, API keys, and "
                        "other secrets that should never leave the server."
                    ),
                    affected_component="/debug endpoint",
                    evidence=(
                        f"GET /debug returned {env_count} environment variables in plaintext.\n"
                        "Sample keys exposed (first 5): "
                        + str(list(data.get("env_vars", {}).keys())[:5])
                    ),
                    impact=(
                        "Complete exposure of server environment including:\n"
                        "  • Database connection strings with passwords\n"
                        "  • Cloud provider access keys\n"
                        "  • Secret keys used for session signing\n"
                        "  • Third-party API credentials\n"
                        "This effectively hands an attacker the keys to the entire infrastructure."
                    ),
                    recommendation=(
                        "1. Remove /debug endpoint immediately in production.\n"
                        "2. Use a secrets manager (HashiCorp Vault, AWS Secrets Manager).\n"
                        "3. Never store secrets in environment variables accessible to the app.\n"
                        "4. If env vars must be used, never expose them via any API endpoint.\n"
                        "5. Audit all endpoints for accidental secret exposure."
                    ),
                    source=FindingSource.REAL,
                    cwe_id="CWE-526",
                    cvss_score=9.8,
                ))

    except requests.RequestException:
        pass

    return findings


def _check_response_data_minimization(target_url: str) -> list[Finding]:
    """
    Check if API responses return more data than the client needs.
    GDPR and privacy best practices require data minimization.
    """
    findings = []

    try:
        r = requests.get(f"{target_url}/api/admin/users", timeout=5)

        if r.status_code == 200:
            data = r.json()
            users = data.get("users", [])

            if users and any("password" in u or "role" in u for u in users):
                findings.append(Finding(
                    id="SEC-STORE-002",
                    title="Sensitive User Data Returned in API Response",
                    category="Data Storage & Privacy",
                    severity=Severity.MEDIUM,
                    description=(
                        "The user listing API returns sensitive fields (role, and potentially "
                        "other internal fields) that should not be exposed to all callers. "
                        "API responses should only contain what the requesting client needs."
                    ),
                    affected_component="/api/admin/users",
                    evidence=(
                        f"GET /api/admin/users returned {len(users)} users with fields: "
                        + str(list(users[0].keys()) if users else [])
                    ),
                    impact=(
                        "Exposing user roles and details allows attackers to identify "
                        "high-privilege accounts and target them for credential attacks."
                    ),
                    recommendation=(
                        "1. Apply data minimization — only return fields needed by the UI.\n"
                        "2. Use response schemas (Pydantic/marshmallow) to control output.\n"
                        "3. Remove sensitive fields from list endpoints.\n"
                        "4. Implement field-level access control based on caller role."
                    ),
                    source=FindingSource.REAL,
                    cwe_id="CWE-213",
                ))

    except requests.RequestException:
        pass

    return findings
