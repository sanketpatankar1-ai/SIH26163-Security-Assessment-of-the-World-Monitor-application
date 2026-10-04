"""
security_engine/demo_data.py
==============================
Demo / Sample Assessment Dataset

These findings are CLEARLY LABELLED as DEMO data.
They are shown when the target app is not running, or when
Demo Mode is enabled.

IMPORTANT: These findings are representative examples of common
web application security issues. They are NOT claims about any
specific real application's vulnerabilities.

Judges can see these immediately on opening the dashboard.
"""

from .finding import Finding, Severity, FindingStatus, FindingSource


def get_demo_findings() -> list[Finding]:
    """
    Return a curated set of demo findings for presentation purposes.
    All are clearly marked source=FindingSource.DEMO.
    """
    return [
        Finding(
            id="SEC-001",
            title="Broken Access Control — Admin Endpoint Exposed",
            category="Authorization",
            severity=Severity.CRITICAL,
            description=(
                "The /api/admin/users endpoint is accessible without authentication "
                "or authorization checks. Any user — including unauthenticated visitors — "
                "can retrieve the complete list of system users and their roles."
            ),
            affected_component="/api/admin/users",
            evidence=(
                "[DEMO] GET /api/admin/users (no auth headers)\n"
                "HTTP 200 OK\n"
                '{"users": [{"username": "admin", "role": "admin"}, ...]}'
            ),
            impact=(
                "Complete exposure of user account data. Enables targeted credential "
                "attacks against administrator accounts. Classified as OWASP Top 10 #1."
            ),
            recommendation=(
                "Implement role-based access control (RBAC). Require valid admin session "
                "before serving any /api/admin/* endpoint. Return HTTP 403 Forbidden "
                "for unauthorized requests."
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.OPEN,
            cwe_id="CWE-285",
            cvss_score=9.1,
        ),
        Finding(
            id="SEC-002",
            title="No Rate Limiting on Login Endpoint",
            category="Authentication",
            severity=Severity.HIGH,
            description=(
                "The /api/login endpoint accepts unlimited authentication requests "
                "without throttling or blocking. This enables automated brute-force "
                "and credential stuffing attacks."
            ),
            affected_component="/api/login",
            evidence=(
                "[DEMO] 6 consecutive POST /api/login requests sent in rapid succession.\n"
                "All returned HTTP 401 — no 429 Too Many Requests detected.\n"
                "No rate limit headers (X-RateLimit-*) present in responses."
            ),
            impact=(
                "Attackers can use automated tools to try millions of password combinations. "
                "Combined with weak credentials (SEC-003), this creates a critical attack path."
            ),
            recommendation=(
                "Implement Flask-Limiter: limit('/api/login', '5 per minute').\n"
                "Add progressive delays after failed attempts.\n"
                "Implement account lockout after 10 consecutive failures."
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.OPEN,
            cwe_id="CWE-307",
        ),
        Finding(
            id="SEC-003",
            title="Weak Default Credentials Accepted",
            category="Authentication",
            severity=Severity.CRITICAL,
            description=(
                "The application accepts the default username 'admin' with password "
                "'admin123'. Default credentials are well-known and are among the first "
                "combinations attackers try."
            ),
            affected_component="/api/login",
            evidence=(
                "[DEMO] POST /api/login with credentials admin:admin123\n"
                'HTTP 200 OK → {"success": true, "role": "admin"}'
            ),
            impact=(
                "Any attacker who tries default credentials gains full administrative "
                "access to World Monitor. This is a trivial attack requiring no skill."
            ),
            recommendation=(
                "Remove all hardcoded/default credentials.\n"
                "Enforce minimum 12-character passwords with complexity requirements.\n"
                "Store passwords using bcrypt (never plaintext or MD5).\n"
                "Force password change on first login."
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.FIXED,
            cwe_id="CWE-521",
            cvss_score=9.8,
        ),
        Finding(
            id="SEC-004",
            title="Missing HTTP Security Headers",
            category="API Security",
            severity=Severity.MEDIUM,
            description=(
                "The application is missing 5 critical HTTP security headers: "
                "X-Frame-Options, X-Content-Type-Options, Content-Security-Policy, "
                "Referrer-Policy, and Permissions-Policy. These headers instruct "
                "browsers to enforce security policies."
            ),
            affected_component="All HTTP Responses",
            evidence=(
                "[DEMO] GET / — Response header analysis:\n"
                "  ✗ X-Frame-Options: MISSING\n"
                "  ✗ X-Content-Type-Options: MISSING\n"
                "  ✗ Content-Security-Policy: MISSING\n"
                "  ✗ Referrer-Policy: MISSING\n"
                "  ✗ Permissions-Policy: MISSING"
            ),
            impact=(
                "Without these headers, the application is vulnerable to:\n"
                "  • Clickjacking (missing X-Frame-Options)\n"
                "  • MIME confusion attacks (missing X-Content-Type-Options)\n"
                "  • XSS attacks (missing Content-Security-Policy)"
            ),
            recommendation=(
                "Add a Flask after_request hook to inject all security headers. "
                "Or use Flask-Talisman which handles all headers automatically in one line."
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.FIXED,
            cwe_id="CWE-693",
        ),
        Finding(
            id="SEC-005",
            title="User Input Reflected Without Sanitization (XSS Indicator)",
            category="Input Validation",
            severity=Severity.MEDIUM,
            description=(
                "The search endpoint (/api/search?q=) reflects the 'q' parameter "
                "directly in the JSON response without encoding. If this data is "
                "rendered in an HTML template, it creates a Reflected XSS vulnerability."
            ),
            affected_component="/api/search?q=",
            evidence=(
                "[DEMO] GET /api/search?q=SECTEST-MARKER\n"
                '{"query": "SECTEST-MARKER", "results": [...], "count": 0}\n'
                "Input value appears verbatim in response body."
            ),
            impact=(
                "An attacker can craft a malicious URL and send it to World Monitor users. "
                "When clicked, JavaScript executes in the victim's browser — enabling "
                "session hijacking, credential theft, and defacement."
            ),
            recommendation=(
                "1. Never reflect raw user input.\n"
                "2. Validate 'q' parameter against an allowlist pattern.\n"
                "3. Use output encoding (html.escape) when inserting into HTML.\n"
                "4. Implement Content-Security-Policy to block inline scripts."
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.OPEN,
            cwe_id="CWE-79",
        ),
        Finding(
            id="SEC-006",
            title="Application Running Over HTTP (No Encryption)",
            category="Communication Security",
            severity=Severity.HIGH,
            description=(
                "The World Monitor application serves all traffic over plain HTTP. "
                "All data — including authentication credentials — is transmitted "
                "in plaintext, visible to any network observer."
            ),
            affected_component="Transport Layer (HTTP)",
            evidence=(
                "[DEMO] Application URL: http://localhost:5001\n"
                "No HTTPS redirect detected.\n"
                "Login POST sends credentials in plaintext over HTTP."
            ),
            impact=(
                "An attacker on the same network can capture all traffic with Wireshark "
                "or similar tools, reading usernames, passwords, and session tokens "
                "as they flow across the network."
            ),
            recommendation=(
                "Deploy behind HTTPS using a TLS certificate (Let's Encrypt is free). "
                "Redirect all HTTP traffic to HTTPS. Add HSTS header. "
                "For development, use mkcert for local HTTPS."
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.ACCEPTED_RISK,
            cwe_id="CWE-319",
            cvss_score=8.8,
        ),
        Finding(
            id="SEC-007",
            title="Debug Endpoint Exposes Environment Variables",
            category="Data Storage & Privacy",
            severity=Severity.CRITICAL,
            description=(
                "A /debug endpoint is publicly accessible and returns all server "
                "environment variables in the response. Environment variables typically "
                "contain database passwords, API keys, and cloud credentials."
            ),
            affected_component="/debug",
            evidence=(
                "[DEMO] GET /debug → HTTP 200\n"
                '{"env_vars": {"PATH": "...", "COMPUTERNAME": "...", ...}, '
                '"config": {"debug": true, "secret_key_length": 21}}'
            ),
            impact=(
                "Full exposure of server configuration including:\n"
                "  • Database connection strings\n"
                "  • Cloud provider access keys\n"
                "  • Session signing secrets\n"
                "This is often a single-step path to complete system compromise."
            ),
            recommendation=(
                "Remove /debug endpoint immediately.\n"
                "Set DEBUG=False in production.\n"
                "Use a secrets manager for sensitive credentials.\n"
                "Audit codebase for other debug/diagnostic endpoints."
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.FIXED,
            cwe_id="CWE-526",
            cvss_score=9.8,
        ),
        Finding(
            id="SEC-008",
            title="Session Cookie Missing HttpOnly and Secure Flags",
            category="Client-Side Security",
            severity=Severity.MEDIUM,
            description=(
                "Session cookies are set without the HttpOnly and Secure flags. "
                "HttpOnly prevents JavaScript from reading cookies (XSS mitigation). "
                "Secure ensures cookies are only sent over HTTPS."
            ),
            affected_component="Session Cookie (Set-Cookie header)",
            evidence=(
                "[DEMO] POST /api/login → Set-Cookie: session=...\n"
                "Flags present: None\n"
                "Missing: HttpOnly, Secure, SameSite"
            ),
            impact=(
                "XSS attacks can steal session cookies (HttpOnly missing).\n"
                "Cookies sent over HTTP (Secure missing).\n"
                "CSRF attacks possible (SameSite missing)."
            ),
            recommendation=(
                "In Flask config:\n"
                "  SESSION_COOKIE_HTTPONLY = True\n"
                "  SESSION_COOKIE_SECURE = True\n"
                "  SESSION_COOKIE_SAMESITE = 'Strict'"
            ),
            source=FindingSource.DEMO,
            status=FindingStatus.FIXED,
            cwe_id="CWE-1004",
        ),
    ]
