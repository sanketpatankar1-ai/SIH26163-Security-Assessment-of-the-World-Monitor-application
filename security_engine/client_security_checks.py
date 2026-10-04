"""
security_engine/client_security_checks.py
===========================================
Client-Side Security Checks

What we check:
  - Sensitive data exposed in API responses unnecessarily
  - Information disclosure in responses
  - Cookie security flags (if applicable)

Note: Full client-side JS analysis would require a browser/headless chrome.
This module performs API-level client security inspection.
"""

import requests
from .finding import Finding, Severity, FindingSource


def run_client_security_checks(target_url: str) -> list[Finding]:
    """Run client-side security checks."""
    findings = []
    findings.extend(_check_sensitive_response_data(target_url))
    findings.extend(_check_cookie_flags(target_url))
    return findings


def _check_sensitive_response_data(target_url: str) -> list[Finding]:
    """
    Check if API responses expose more data than necessary.
    Principle: APIs should return only the minimum required data.
    """
    findings = []

    try:
        r = requests.get(f"{target_url}/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            sensitive_keys = ["server", "environment", "version", "debug"]
            exposed = [k for k in sensitive_keys if k in data]

            if exposed:
                findings.append(Finding(
                    id="SEC-CLIENT-001",
                    title="Unnecessary Information Disclosure in API Response",
                    category="Client-Side Security",
                    severity=Severity.LOW,
                    description=(
                        "The API home endpoint returns unnecessary technical information "
                        "including server technology, version, and environment details. "
                        "This violates the principle of minimal information exposure."
                    ),
                    affected_component="/ (home endpoint JSON response)",
                    evidence=(
                        f"GET {target_url}/ returns fields: {exposed}\n"
                        f"Response: {r.text[:400]}"
                    ),
                    impact=(
                        "Exposed server/version information helps attackers identify "
                        "specific software versions and look up known CVEs to exploit."
                    ),
                    recommendation=(
                        "1. Remove non-essential fields from public API responses.\n"
                        "2. Only return data that the client genuinely needs.\n"
                        "3. Move sensitive config to server-side logs, not API responses."
                    ),
                    source=FindingSource.REAL,
                    cwe_id="CWE-200",
                ))

    except requests.RequestException:
        pass

    return findings


def _check_cookie_flags(target_url: str) -> list[Finding]:
    """
    Check if session cookies have secure flags set.
    HttpOnly prevents JS from reading the cookie.
    Secure ensures cookie only sent over HTTPS.
    SameSite prevents CSRF.
    """
    findings = []

    try:
        r = requests.post(
            f"{target_url}/api/login",
            json={"username": "admin", "password": "admin123"},
            timeout=5,
        )

        set_cookie = r.headers.get("Set-Cookie", "")

        if set_cookie:
            issues = []
            if "HttpOnly" not in set_cookie:
                issues.append("Missing HttpOnly flag — JavaScript can access this cookie")
            if "Secure" not in set_cookie:
                issues.append("Missing Secure flag — Cookie sent over HTTP too")
            if "SameSite" not in set_cookie:
                issues.append("Missing SameSite flag — Vulnerable to CSRF attacks")

            if issues:
                findings.append(Finding(
                    id="SEC-CLIENT-002",
                    title="Session Cookie Missing Security Flags",
                    category="Client-Side Security",
                    severity=Severity.MEDIUM,
                    description=(
                        "Session cookies are set without essential security flags. "
                        "Missing HttpOnly, Secure, and SameSite flags weaken cookie "
                        "security and enable session theft attacks."
                    ),
                    affected_component="Session Cookie (Set-Cookie header)",
                    evidence=(
                        f"Set-Cookie header: {set_cookie[:200]}\n"
                        "Issues found:\n" + "\n".join(f"  • {i}" for i in issues)
                    ),
                    impact=(
                        "Without HttpOnly, XSS can steal cookies.\n"
                        "Without Secure, cookies travel over HTTP.\n"
                        "Without SameSite, CSRF attacks are possible."
                    ),
                    recommendation=(
                        "Set all three flags on session cookies:\n"
                        "  Set-Cookie: session=...; HttpOnly; Secure; SameSite=Strict\n\n"
                        "In Flask:\n"
                        "  SESSION_COOKIE_HTTPONLY = True\n"
                        "  SESSION_COOKIE_SECURE = True\n"
                        "  SESSION_COOKIE_SAMESITE = 'Strict'"
                    ),
                    source=FindingSource.REAL,
                    cwe_id="CWE-1004",
                ))

    except requests.RequestException:
        pass

    return findings
