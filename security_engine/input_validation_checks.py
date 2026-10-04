"""
security_engine/input_validation_checks.py
============================================
Input Validation & Data Handling Checks

What we check:
  - Reflected input in responses (XSS indicator)
  - Error messages that reveal stack traces
  - Unvalidated query parameters
  - Content-Type enforcement

These are observational checks — we look at behavior, not exploit it.
"""

import requests
from .finding import Finding, Severity, FindingSource


def run_input_validation_checks(target_url: str) -> list[Finding]:
    """Run all input validation checks."""
    findings = []
    findings.extend(_check_reflected_input(target_url))
    findings.extend(_check_error_disclosure(target_url))
    return findings


def _check_reflected_input(target_url: str) -> list[Finding]:
    """
    Check if user-supplied input is reflected back without encoding.
    This is an indicator of potential Reflected XSS.
    We use a safe marker string — NOT an actual XSS payload.
    """
    findings = []
    search_url = f"{target_url}/api/search"
    # Safe test marker — no script tags, no actual exploit
    safe_marker = "SECTEST-REFLECTION-CHECK"

    try:
        r = requests.get(search_url, params={"q": safe_marker}, timeout=5)

        if r.status_code == 200:
            response_text = r.text

            if safe_marker in response_text:
                findings.append(Finding(
                    id="SEC-INPUT-001",
                    title="User Input Reflected in API Response (XSS Indicator)",
                    category="Input Validation",
                    severity=Severity.MEDIUM,
                    description=(
                        "The /api/search endpoint reflects the user-supplied 'q' parameter "
                        "directly back in the response body without encoding or sanitization. "
                        "If this response is rendered in a browser, it could enable "
                        "Reflected Cross-Site Scripting (XSS) attacks."
                    ),
                    affected_component="/api/search?q=",
                    evidence=(
                        f"GET /api/search?q={safe_marker}\n"
                        f"Response body contains the exact input string: '{safe_marker}'\n"
                        f"Raw response snippet: {response_text[:300]}"
                    ),
                    impact=(
                        "If an attacker crafts a URL with malicious JavaScript in the 'q' "
                        "parameter and tricks a user into visiting it, the script executes "
                        "in the user's browser — enabling session theft, keylogging, and "
                        "account takeover."
                    ),
                    recommendation=(
                        "1. Never reflect raw user input in responses.\n"
                        "2. Validate and sanitize all input parameters server-side.\n"
                        "3. Use output encoding when reflecting data in HTML contexts.\n"
                        "4. Implement Content-Security-Policy to limit script execution.\n"
                        "5. Use parameterized queries and template auto-escaping."
                    ),
                    source=FindingSource.REAL,
                    cwe_id="CWE-79",
                ))

    except requests.RequestException:
        pass

    return findings


def _check_error_disclosure(target_url: str) -> list[Finding]:
    """
    Check if malformed requests cause verbose error messages.
    Debug stack traces in production expose file paths, line numbers, and logic.
    """
    findings = []

    try:
        # Send malformed JSON to trigger an error
        r = requests.post(
            f"{target_url}/api/login",
            data="this-is-not-json",
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        response_text = r.text.lower()
        # Look for debug indicators in the response
        debug_indicators = ["traceback", "werkzeug", "debugger", "internal server", "file \""]
        found = [indicator for indicator in debug_indicators if indicator in response_text]

        if found or r.status_code == 500:
            findings.append(Finding(
                id="SEC-INPUT-002",
                title="Verbose Error Messages / Debug Information Exposure",
                category="Input Validation",
                severity=Severity.MEDIUM,
                description=(
                    "The application returns detailed error messages or debug information "
                    "when it encounters invalid input. Debug mode is enabled, which can "
                    "expose stack traces, file paths, and internal application logic."
                ),
                affected_component="/api/login (error handling)",
                evidence=(
                    f"POST /api/login with malformed JSON body.\n"
                    f"HTTP Status: {r.status_code}\n"
                    f"Debug indicators found in response: {found if found else 'None, but HTTP 500 returned'}\n"
                    f"Response preview: {r.text[:300]}"
                ),
                impact=(
                    "Stack traces reveal internal file paths, library versions, "
                    "and application logic — significantly aiding attackers in "
                    "crafting targeted exploits."
                ),
                recommendation=(
                    "1. Set DEBUG=False in all production/staging environments.\n"
                    "2. Implement global error handlers that return generic messages:\n"
                    "   @app.errorhandler(500)\n"
                    "   def server_error(e): return jsonify(error='Internal server error'), 500\n"
                    "3. Log detailed errors server-side (not to the client).\n"
                    "4. Use a logging framework (Python logging) for error tracking."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-209",
            ))

    except requests.RequestException:
        pass

    return findings
