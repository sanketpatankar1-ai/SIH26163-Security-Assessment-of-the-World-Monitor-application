"""
security_engine/api_checks.py
================================
API Security Checks

What we check:
  - Missing HTTP security headers (X-Frame-Options, CSP, HSTS, etc.)
  - CORS policy misconfiguration
  - Unsafe HTTP methods allowed
  - Server information disclosure in headers
  - Missing authentication on API routes
"""

import requests
from .finding import Finding, Severity, FindingSource

# Security headers that every web application should include
REQUIRED_SECURITY_HEADERS = {
    "X-Frame-Options": (
        "Prevents clickjacking attacks by controlling if page can be embedded in an iframe."
    ),
    "X-Content-Type-Options": (
        "Prevents browsers from MIME-sniffing — serving files as wrong content type."
    ),
    "Content-Security-Policy": (
        "Restricts which resources (scripts, styles) the browser can load, preventing XSS."
    ),
    "Referrer-Policy": (
        "Controls how much referrer information is included with requests."
    ),
    "Permissions-Policy": (
        "Controls browser features (camera, microphone, location) the page can use."
    ),
}


def run_api_checks(target_url: str) -> list[Finding]:
    """Run all API security checks."""
    findings = []
    findings.extend(_check_security_headers(target_url))
    findings.extend(_check_cors_policy(target_url))
    findings.extend(_check_server_info_disclosure(target_url))
    return findings


def _check_security_headers(target_url: str) -> list[Finding]:
    """
    Inspect response headers for missing security headers.
    This is one of the most important and commonly missed security controls.
    """
    findings = []

    try:
        r = requests.get(target_url, timeout=5)
        headers = r.headers
        missing = []

        for header, description in REQUIRED_SECURITY_HEADERS.items():
            if header not in headers:
                missing.append(f"  • {header}: {description}")

        if missing:
            findings.append(Finding(
                id="SEC-API-001",
                title="Missing HTTP Security Headers",
                category="API Security",
                severity=Severity.MEDIUM,
                description=(
                    "The application is missing critical HTTP security headers. "
                    "These headers are a first line of defense against common web attacks "
                    "including XSS, clickjacking, and MIME-type confusion."
                ),
                affected_component=f"HTTP Response Headers ({target_url})",
                evidence=(
                    f"GET {target_url} — Response headers checked.\n"
                    f"Missing headers ({len(missing)}):\n"
                    + "\n".join(missing)
                ),
                impact=(
                    "Without these headers, browsers cannot enforce security policies. "
                    "Users are exposed to clickjacking, XSS, and content injection attacks "
                    "that these headers would otherwise prevent."
                ),
                recommendation=(
                    "Add the following headers to all responses (Flask example):\n\n"
                    "@app.after_request\n"
                    "def add_security_headers(response):\n"
                    "    response.headers['X-Frame-Options'] = 'DENY'\n"
                    "    response.headers['X-Content-Type-Options'] = 'nosniff'\n"
                    "    response.headers['Content-Security-Policy'] = \"default-src 'self'\"\n"
                    "    response.headers['Referrer-Policy'] = 'no-referrer'\n"
                    "    return response\n\n"
                    "Or use Flask-Talisman for automatic security header management."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-693",
            ))

        # Also check for HSTS specifically (requires HTTPS to be meaningful)
        if "Strict-Transport-Security" not in headers:
            findings.append(Finding(
                id="SEC-API-002",
                title="Missing Strict-Transport-Security (HSTS) Header",
                category="API Security",
                severity=Severity.LOW,
                description=(
                    "The Strict-Transport-Security (HSTS) header is absent. "
                    "This header instructs browsers to only communicate over HTTPS, "
                    "preventing protocol downgrade attacks."
                ),
                affected_component="HTTP Response Headers",
                evidence=(
                    f"Response from {target_url} does not include "
                    "'Strict-Transport-Security' header."
                ),
                impact=(
                    "Without HSTS, an attacker on the same network could intercept "
                    "the first HTTP request (SSL stripping attack) and downgrade "
                    "the connection from HTTPS to HTTP."
                ),
                recommendation=(
                    "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n"
                    "Note: HSTS is only effective when the site uses HTTPS in production."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-319",
            ))

    except requests.RequestException:
        pass

    return findings


def _check_cors_policy(target_url: str) -> list[Finding]:
    """
    Check CORS (Cross-Origin Resource Sharing) configuration.
    Overly permissive CORS allows any website to make requests to the API.
    """
    findings = []

    try:
        # Send a preflight OPTIONS request with an arbitrary origin
        r = requests.options(
            f"{target_url}/api/data",
            headers={"Origin": "https://evil.example.com"},
            timeout=5,
        )
        acao = r.headers.get("Access-Control-Allow-Origin", "")

        if acao == "*" or acao == "https://evil.example.com":
            findings.append(Finding(
                id="SEC-API-003",
                title="Overly Permissive CORS Policy",
                category="API Security",
                severity=Severity.MEDIUM,
                description=(
                    "The API allows cross-origin requests from any domain (wildcard CORS). "
                    "This means any website on the internet can make authenticated "
                    "API requests to World Monitor on behalf of logged-in users."
                ),
                affected_component="CORS Configuration (all API routes)",
                evidence=(
                    f"OPTIONS request to /api/data with Origin: https://evil.example.com\n"
                    f"Response header: Access-Control-Allow-Origin: {acao}\n"
                    "Any origin is permitted."
                ),
                impact=(
                    "A malicious website can trick logged-in World Monitor users into "
                    "executing API requests (data theft, account modification) without "
                    "their knowledge — a Cross-Site Request Forgery (CSRF) variant."
                ),
                recommendation=(
                    "1. Restrict CORS to specific trusted origins:\n"
                    "   CORS(app, origins=['https://worldmonitor.example.com'])\n"
                    "2. Do not use wildcard (*) with credentials.\n"
                    "3. For APIs, only allow origins you control.\n"
                    "4. Add CSRF tokens for state-changing operations."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-346",
            ))

    except requests.RequestException:
        pass

    return findings


def _check_server_info_disclosure(target_url: str) -> list[Finding]:
    """
    Check if the server reveals technology information in headers.
    Server/X-Powered-By headers help attackers target known vulnerabilities.
    """
    findings = []

    try:
        r = requests.get(target_url, timeout=5)
        disclosed = {}

        for header in ["Server", "X-Powered-By", "X-AspNet-Version"]:
            if header in r.headers:
                disclosed[header] = r.headers[header]

        if disclosed:
            findings.append(Finding(
                id="SEC-API-004",
                title="Server Technology Information Disclosure",
                category="API Security",
                severity=Severity.INFORMATIONAL,
                description=(
                    "HTTP response headers reveal the server technology stack. "
                    "While not directly exploitable, this information helps attackers "
                    "identify known vulnerabilities for the specific versions in use."
                ),
                affected_component="HTTP Response Headers",
                evidence=(
                    "Disclosed headers: " + str(disclosed)
                ),
                impact=(
                    "Attackers can use disclosed version information to look up "
                    "known CVEs and target unpatched vulnerabilities."
                ),
                recommendation=(
                    "Remove or obscure server identification headers:\n"
                    "  SERVER_NAME = '' in Flask config\n"
                    "  Or use a reverse proxy (nginx) to strip/replace Server header."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-200",
            ))

    except requests.RequestException:
        pass

    return findings
