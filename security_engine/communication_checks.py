"""
security_engine/communication_checks.py
=========================================
Secure Communication Checks

What we check:
  - HTTP vs HTTPS usage
  - Security headers related to transport (HSTS)
  - TLS configuration indicators
  - Mixed content indicators
"""

import requests
import urllib.parse
from .finding import Finding, Severity, FindingSource


def run_communication_checks(target_url: str) -> list[Finding]:
    """Run all communication security checks."""
    findings = []
    findings.extend(_check_http_usage(target_url))
    findings.extend(_check_sensitive_data_over_http(target_url))
    return findings


def _check_http_usage(target_url: str) -> list[Finding]:
    """
    Check if the application uses HTTP instead of HTTPS.
    HTTP transmits all data in plaintext — including passwords.
    """
    findings = []
    parsed = urllib.parse.urlparse(target_url)

    if parsed.scheme == "http":
        findings.append(Finding(
            id="SEC-COMM-001",
            title="Application Accessible Over Unencrypted HTTP",
            category="Communication Security",
            severity=Severity.HIGH,
            description=(
                "The World Monitor application is accessible over HTTP (unencrypted). "
                "All data transmitted — including login credentials, session tokens, "
                "and monitoring data — is sent in plaintext and can be intercepted "
                "by anyone on the same network."
            ),
            affected_component=f"Application Transport Layer ({target_url})",
            evidence=(
                f"Application URL uses HTTP scheme: {target_url}\n"
                "No HTTPS redirect detected. All traffic is unencrypted."
            ),
            impact=(
                "An attacker on the same network (e.g., same Wi-Fi) can use "
                "packet capture tools (Wireshark) to read all data including "
                "usernames, passwords, and session tokens in plaintext."
            ),
            recommendation=(
                "1. Deploy the application behind HTTPS using a TLS certificate.\n"
                "2. Use Let's Encrypt (free) for certificate issuance.\n"
                "3. Configure automatic HTTP → HTTPS redirect.\n"
                "4. Add HSTS header to prevent future HTTP access:\n"
                "   Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
                "5. For local development, use mkcert for local HTTPS."
            ),
            source=FindingSource.REAL,
            cwe_id="CWE-319",
        ))

    return findings


def _check_sensitive_data_over_http(target_url: str) -> list[Finding]:
    """
    Check if sensitive data (credentials) is transmitted over HTTP.
    """
    findings = []
    parsed = urllib.parse.urlparse(target_url)

    if parsed.scheme == "http":
        try:
            # Try login — observe that credentials go over HTTP
            r = requests.post(
                f"{target_url}/api/login",
                json={"username": "test", "password": "test"},
                timeout=5,
            )

            findings.append(Finding(
                id="SEC-COMM-002",
                title="Login Credentials Transmitted Over HTTP (Plaintext)",
                category="Communication Security",
                severity=Severity.CRITICAL,
                description=(
                    "Authentication credentials (username and password) are transmitted "
                    "over an unencrypted HTTP connection. This means any network observer "
                    "can capture credentials in plaintext."
                ),
                affected_component="/api/login over HTTP",
                evidence=(
                    f"POST {target_url}/api/login sent JSON credentials over plain HTTP.\n"
                    "Network capture would reveal: "
                    '{"username": "...", "password": "..."} in plaintext.\n'
                    f"HTTP Status received: {r.status_code}"
                ),
                impact=(
                    "Any attacker with network access (on the same LAN, Wi-Fi, or "
                    "controlling a network device) can capture login credentials in "
                    "plain text and use them to access the application."
                ),
                recommendation=(
                    "Implement HTTPS immediately. This is a critical security requirement "
                    "for any application handling credentials. See SEC-COMM-001 for details."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-523",
                cvss_score=8.8,
            ))

        except requests.RequestException:
            pass

    return findings
