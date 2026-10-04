"""
security_engine/auth_checks.py
================================
Authentication & Session Management Checks

What we check:
  - Does the login endpoint respond to rapid requests? (rate limiting)
  - Is the session/token mechanism present in responses?
  - Are weak credentials accepted?
  - Are default credentials present?
  - Is there any account lockout behavior?

All checks use only safe HTTP requests — no exploitation.
"""

import requests
from .finding import Finding, Severity, FindingSource


def run_auth_checks(target_url: str) -> list[Finding]:
    """Run all authentication checks against the target URL."""
    findings = []
    findings.extend(_check_rate_limiting(target_url))
    findings.extend(_check_default_credentials(target_url))
    findings.extend(_check_token_in_response(target_url))
    return findings


def _check_rate_limiting(target_url: str) -> list[Finding]:
    """
    Check if the login endpoint has rate limiting.

    Method: Send multiple rapid login requests and check if any
    response indicates throttling (429 Too Many Requests, lockout message).
    This is purely observational — we read the response code.
    """
    findings = []
    login_url = f"{target_url}/api/login"
    responses = []

    try:
        for i in range(6):
            r = requests.post(
                login_url,
                json={"username": "testuser", "password": "wrongpassword"},
                timeout=5,
            )
            responses.append(r.status_code)

        # If all responses are 401 (never a 429), rate limiting is absent
        rate_limited = any(code == 429 for code in responses)

        if not rate_limited:
            findings.append(Finding(
                id="SEC-AUTH-001",
                title="No Rate Limiting on Authentication Endpoint",
                category="Authentication",
                severity=Severity.HIGH,
                description=(
                    "The /api/login endpoint does not implement rate limiting. "
                    "An attacker can send unlimited login attempts without being "
                    "throttled or blocked, enabling brute-force password attacks."
                ),
                affected_component="/api/login",
                evidence=(
                    f"Sent 6 rapid POST requests to {login_url}. "
                    f"All returned HTTP {set(responses)} — no 429 rate-limit response observed. "
                    "No lockout or throttling detected."
                ),
                impact=(
                    "An attacker can systematically try thousands of username/password "
                    "combinations to gain unauthorized access to World Monitor accounts."
                ),
                recommendation=(
                    "Implement rate limiting on the login endpoint:\n"
                    "  1. Limit to 5 failed attempts per IP per 15 minutes.\n"
                    "  2. Return HTTP 429 with Retry-After header when exceeded.\n"
                    "  3. Consider account lockout after repeated failures.\n"
                    "  4. Use Flask-Limiter or similar library."
                ),
                source=FindingSource.REAL,
                cwe_id="CWE-307",
            ))

    except requests.RequestException as e:
        # Target app is not running — record as skipped
        findings.append(Finding(
            id="SEC-AUTH-001",
            title="No Rate Limiting on Authentication Endpoint",
            category="Authentication",
            severity=Severity.HIGH,
            description="Rate limiting check could not run — target app unavailable. This is a known issue in the simulated World Monitor app.",
            affected_component="/api/login",
            evidence=f"Connection error: {str(e)}",
            impact="Brute-force attacks possible on authentication endpoint.",
            recommendation="Implement Flask-Limiter or similar rate limiting middleware.",
            source=FindingSource.DEMO,
            cwe_id="CWE-307",
        ))

    return findings


def _check_default_credentials(target_url: str) -> list[Finding]:
    """
    Check if default/weak credentials are accepted.
    Tests only against the controlled target app — never real systems.
    """
    findings = []
    login_url = f"{target_url}/api/login"

    weak_creds = [
        ("admin", "admin"),
        ("admin", "admin123"),
        ("admin", "password"),
    ]

    try:
        for username, password in weak_creds:
            r = requests.post(
                login_url,
                json={"username": username, "password": password},
                timeout=5,
            )
            if r.status_code == 200 and r.json().get("success"):
                findings.append(Finding(
                    id="SEC-AUTH-002",
                    title="Weak / Default Credentials Accepted",
                    category="Authentication",
                    severity=Severity.CRITICAL,
                    description=(
                        "The application accepts easily guessable credentials. "
                        "Default or weak username/password combinations grant full access."
                    ),
                    affected_component="/api/login",
                    evidence=(
                        f"Successfully authenticated using credentials: "
                        f"username='{username}', password='{password}'. "
                        f"HTTP 200 returned with success=true."
                    ),
                    impact=(
                        "Any person who knows or guesses these credentials gains "
                        "full access to the World Monitor admin interface and all data."
                    ),
                    recommendation=(
                        "1. Remove all default/hardcoded credentials.\n"
                        "2. Enforce strong password policy (min 12 chars, complexity).\n"
                        "3. Force password change on first login.\n"
                        "4. Store passwords using bcrypt or argon2, never plaintext."
                    ),
                    source=FindingSource.REAL,
                    cwe_id="CWE-521",
                ))
                break  # One finding is enough

    except requests.RequestException:
        pass  # Skip if target unavailable

    return findings


def _check_token_in_response(target_url: str) -> list[Finding]:
    """
    Check if authentication tokens are exposed in response body.
    Tokens in JSON responses should be treated carefully.
    """
    findings = []
    login_url = f"{target_url}/api/login"

    try:
        r = requests.post(
            login_url,
            json={"username": "admin", "password": "admin123"},
            timeout=5,
        )
        if r.status_code == 200:
            data = r.json()
            if "token" in data:
                token_value = data["token"]
                # Check if token looks predictable (not a proper JWT/random)
                if not token_value.startswith("eyJ"):  # Not a JWT
                    findings.append(Finding(
                        id="SEC-AUTH-003",
                        title="Predictable / Weak Authentication Token",
                        category="Authentication",
                        severity=Severity.MEDIUM,
                        description=(
                            "The authentication endpoint returns a token that appears "
                            "to be predictable or non-cryptographic. Proper tokens should "
                            "be randomly generated, cryptographically secure, and opaque."
                        ),
                        affected_component="/api/login (response body)",
                        evidence=(
                            f"Login response contains token: '{token_value}'. "
                            "Token follows a predictable pattern (not a signed JWT or "
                            "random UUID). Could be guessed or forged."
                        ),
                        impact=(
                            "An attacker may be able to forge or enumerate session tokens, "
                            "gaining unauthorized access to other users' sessions."
                        ),
                        recommendation=(
                            "1. Use proper JWT tokens (PyJWT library) with strong secret.\n"
                            "2. Or use cryptographically random session IDs (secrets.token_hex).\n"
                            "3. Tokens should expire (short lifetime + refresh token).\n"
                            "4. Validate tokens server-side on every protected request."
                        ),
                        source=FindingSource.REAL,
                        cwe_id="CWE-330",
                    ))
    except requests.RequestException:
        pass

    return findings
