"""
target_app/app.py
=================
Simulated "World Monitor" Web Application
------------------------------------------
This is a deliberately simplified web application that represents the
World Monitor system for prototype demonstration purposes.

IMPORTANT: This app is intentionally configured with common security
weaknesses so our assessment engine can detect and report them.
These weaknesses exist ONLY in this controlled prototype target.

DO NOT use this code as a template for real applications.

Security weaknesses present (intentional, for demo):
  - Missing HTTP security headers
  - Debug mode enabled (exposes stack traces)
  - Weak CORS policy (allows all origins)
  - No rate limiting on authentication endpoint
  - Predictable session secret key pattern
  - Exposed /debug endpoint
  - No input sanitization on search endpoint
  - Sensitive data in API response (simulated)
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os

# ─── App Configuration ────────────────────────────────────────────────────────
app = Flask(__name__)

# WEAKNESS 1: Weak, hardcoded secret key (should be long, random, from env)
app.secret_key = "worldmonitor-secret"

# WEAKNESS 2: Debug mode ON exposes stack traces in production
app.config["DEBUG"] = True

# WEAKNESS 3: Overly permissive CORS — accepts requests from any origin
CORS(app, resources={r"/*": {"origins": "*"}})

# ─── Simulated in-memory user store ──────────────────────────────────────────
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "viewer": {"password": "viewer123", "role": "viewer"},
}

# ─── Simulated monitoring data ────────────────────────────────────────────────
MONITOR_DATA = [
    {"id": 1, "location": "Mumbai", "sensor": "AQI", "value": 145, "status": "warning"},
    {"id": 2, "location": "Delhi",  "sensor": "AQI", "value": 210, "status": "critical"},
    {"id": 3, "location": "Pune",   "sensor": "AQI", "value": 72,  "status": "normal"},
]

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Home route — returns basic app info."""
    return jsonify({
        "app": "World Monitor",
        "version": "1.0.0",
        "status": "running",
        # WEAKNESS 4: Unnecessary info disclosure in response
        "server": "Flask/3.0",
        "environment": "development",
    })


@app.route("/api/login", methods=["POST"])
def login():
    """
    Authentication endpoint.
    WEAKNESS 5: No rate limiting — brute force is possible.
    WEAKNESS 6: Generic error message still leaks valid/invalid username info
                via timing (not shown here but common pattern).
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    user = USERS.get(username)
    if user and user["password"] == password:
        session["user"] = username
        session["role"] = user["role"]
        return jsonify({"success": True, "role": user["role"], "token": f"demo-token-{username}"})

    return jsonify({"success": False, "error": "Invalid credentials"}), 401


@app.route("/api/data", methods=["GET"])
def get_data():
    """
    Protected monitoring data endpoint.
    WEAKNESS 7: No proper authorization check — any request returns data.
    In a real app, we would verify a valid session/token here.
    """
    # Note: session check is intentionally weak for demo
    return jsonify({"data": MONITOR_DATA, "total": len(MONITOR_DATA)})


@app.route("/api/search", methods=["GET"])
def search():
    """
    Search endpoint.
    WEAKNESS 8: Query parameter is reflected directly in the response
    without sanitization — reflected XSS indicator.
    """
    query = request.args.get("q", "")
    results = [d for d in MONITOR_DATA if query.lower() in d["location"].lower()]
    return jsonify({
        "query": query,        # Raw reflection of user input
        "results": results,
        "count": len(results),
    })


@app.route("/api/admin/users", methods=["GET"])
def admin_users():
    """
    Admin-only endpoint.
    WEAKNESS 9: No authorization enforcement — any caller gets user list.
    """
    # Should check: if session.get("role") != "admin": abort(403)
    return jsonify({
        "users": [
            {"username": "admin", "role": "admin"},
            {"username": "viewer", "role": "viewer"},
        ]
    })


@app.route("/debug", methods=["GET"])
def debug_info():
    """
    WEAKNESS 10: Exposed debug endpoint leaks environment information.
    This should never exist in production.
    """
    return jsonify({
        "env_vars": dict(os.environ),   # Leaks all environment variables!
        "config": {
            "debug": app.config.get("DEBUG"),
            "secret_key_length": len(app.secret_key),
        },
    })


@app.route("/api/health", methods=["GET"])
def health():
    """Health check — acceptable to expose."""
    return jsonify({"status": "ok", "app": "World Monitor"})


# ─── Security Headers (intentionally missing) ─────────────────────────────────
# WEAKNESS 11: No after_request hook adding security headers.
# A secure app would add:
#   X-Frame-Options: DENY
#   X-Content-Type-Options: nosniff
#   Content-Security-Policy: ...
#   Strict-Transport-Security: ...
#   Referrer-Policy: no-referrer
# These are absent here so our scanner can detect and report them.

if __name__ == "__main__":
    print("=" * 60)
    print("  Simulated World Monitor Application")
    print("  [FOR PROTOTYPE/DEMO USE ONLY]")
    print("  Running on: http://localhost:5001")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5001, debug=True)
