# Security Checks Reference Manual

This catalog lists all security checks executed by the **Security Assessment Engine**.

---

## 1. Authentication (`auth_checks.py`)

### `SEC-AUTH-001`: No Rate Limiting on Authentication Endpoint
- **Severity**: High (-8 points)
- **CWE**: CWE-307 (Improper Restriction of Excessive Authentication Attempts)
- **Check Logic**: Sends 6 consecutive rapid POST requests to `/api/login`. Verifies if any request yields an HTTP 429 (Too Many Requests) or lockout indicator.
- **Evidence Gathered**: HTTP response status distribution and absence of rate-limit throttling headers.
- **Remediation**: Integrate middleware such as `Flask-Limiter` or Redis token-bucket throttling; lock accounts after 5 failed attempts.

### `SEC-AUTH-002`: Weak / Default Credentials Accepted
- **Severity**: Critical (-15 points)
- **CWE**: CWE-521 (Weak Password Requirements)
- **Check Logic**: Tests default combinations (e.g., `admin:admin123`) against the controlled target.
- **Evidence Gathered**: Successful HTTP 200 with authentication token returned.
- **Remediation**: Invalidate all default credentials, enforce complexity requirements (minimum 12 chars), and require credential change on first boot.

### `SEC-AUTH-003`: Predictable Authentication Token
- **Severity**: Medium (-4 points)
- **CWE**: CWE-330 (Use of Insufficiently Random Values)
- **Check Logic**: Evaluates the entropy and format of the issued authentication token.
- **Evidence Gathered**: Pattern inspection indicating non-cryptographic or predictable tokens.
- **Remediation**: Use signed, industry-standard JWTs (JSON Web Tokens) or cryptographically secure 256-bit random session identifiers.

---

## 2. Authorization (`authorization_checks.py`)

### `SEC-AUTHZ-001`: Unauthenticated Access to Protected Data Endpoint
- **Severity**: High (-8 points)
- **CWE**: CWE-862 (Missing Authorization)
- **Check Logic**: Sends unauthenticated GET request to `/api/data`.
- **Evidence Gathered**: HTTP 200 response containing operational sensor readings without token or cookie verification.
- **Remediation**: Enforce route authentication guards (`@login_required` or token validation dependencies).

### `SEC-AUTHZ-002`: Admin Endpoint Accessible Without Authorization
- **Severity**: Critical (-15 points)
- **CWE**: CWE-285 (Improper Authorization)
- **Check Logic**: Sends unauthenticated request to `/api/admin/users`.
- **Evidence Gathered**: HTTP 200 containing user listings and account roles.
- **Remediation**: Implement strict Role-Based Access Control (RBAC); reject non-admin sessions with HTTP 403 Forbidden.

### `SEC-AUTHZ-003`: Debug Endpoint Exposed
- **Severity**: High (-8 points)
- **CWE**: CWE-215 (Insertion of Sensitive Information Into Debugging Code)
- **Check Logic**: Queries `/debug`.
- **Evidence Gathered**: HTTP 200 exposing environment variables and configuration objects.
- **Remediation**: Remove or strictly IP-restrict all debug routes prior to production release; enforce `DEBUG=False`.

---

## 3. API Security (`api_checks.py`)

### `SEC-API-001`: Missing HTTP Security Headers
- **Severity**: Medium (-4 points)
- **CWE**: CWE-693 (Protection Mechanism Failure)
- **Headers Verified**: `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`, `Referrer-Policy`, `Permissions-Policy`.
- **Remediation**: Add headers via response hooks or security middleware (e.g. `Flask-Talisman`).

### `SEC-API-002`: Missing Strict-Transport-Security (HSTS)
- **Severity**: Low (-1 point)
- **CWE**: CWE-319 (Cleartext Transmission of Sensitive Information)
- **Remediation**: Issue `Strict-Transport-Security: max-age=31536000; includeSubDomains`.

### `SEC-API-003`: Overly Permissive CORS Policy
- **Severity**: Medium (-4 points)
- **CWE**: CWE-346 (Origin Validation Error)
- **Check Logic**: Sends preflight `OPTIONS` request with arbitrary foreign origin.
- **Evidence Gathered**: `Access-Control-Allow-Origin: *` returned.
- **Remediation**: Restrict CORS origins to explicitly trusted domain allowlists.

---

## 4. Input Validation (`input_validation_checks.py`)

### `SEC-INPUT-001`: User Input Reflected in API Response
- **Severity**: Medium (-4 points)
- **CWE**: CWE-79 (Cross-Site Scripting)
- **Check Logic**: Submits safe marker string into search parameters and checks for unencoded reflection.
- **Remediation**: Apply contextual output encoding and parameterized input handling.

### `SEC-INPUT-002`: Verbose Error / Debug Information Exposure
- **Severity**: Medium (-4 points)
- **CWE**: CWE-209 (Generation of Error Message Containing Sensitive Information)
- **Remediation**: Implement generic global error handlers and log internal stack traces privately.

---

## 5. Communication Security (`communication_checks.py`)

### `SEC-COMM-001`: Application Accessible Over Unencrypted HTTP
- **Severity**: High (-8 points)
- **CWE**: CWE-319 (Cleartext Transmission)
- **Remediation**: Enforce TLS 1.3 encryption across all communication channels.

### `SEC-COMM-002`: Plaintext Credential Transmission
- **Severity**: Critical (-15 points)
- **CWE**: CWE-523 (Unprotected Transport of Credentials)
- **Remediation**: Ensure authentication requests are strictly routed over HTTPS.

---

## 6. Client-Side Security (`client_security_checks.py`)

### `SEC-CLIENT-002`: Session Cookie Missing Security Flags
- **Severity**: Medium (-4 points)
- **CWE**: CWE-1004 (Sensitive Cookie Without 'HttpOnly' Flag)
- **Flags Checked**: `HttpOnly`, `Secure`, `SameSite`.
- **Remediation**: Configure `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SECURE=True`, and `SESSION_COOKIE_SAMESITE='Strict'`.

---

## 7. Data Storage & Privacy (`storage_checks.py`)

### `SEC-STORE-001`: Environment Variables Exposed via Diagnostic Route
- **Severity**: Critical (-15 points)
- **CWE**: CWE-526 (Exposure of Sensitive Information Through Environmental Variables)
- **Remediation**: Employ secure secrets management tools (e.g. HashiCorp Vault) and prevent any runtime exposure of server environments.
