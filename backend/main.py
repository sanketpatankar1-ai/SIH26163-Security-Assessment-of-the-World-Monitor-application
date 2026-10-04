"""
backend/main.py
================
FastAPI Application Entry Point

This is the main server. It:
  1. Creates the FastAPI app instance
  2. Configures CORS (so the React frontend can connect)
  3. Registers all routers
  4. Seeds the database on startup
  5. Provides the auto-generated Swagger UI at /docs

To run:
  cd sih26163-security-dashboard
  uvicorn backend.main:app --reload --port 8000
"""

import sys
import os

# Add project root to path so security_engine can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.routes.findings import router as findings_router
from backend.routes.assessment import router as assessment_router
from backend.routes.report import router as report_router


# ─── App Instance ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="SIH26163 — World Monitor Security Assessment Platform",
    description=(
        "A prototype security assessment platform for the World Monitor application. "
        "Built for Smart India Hackathon 2026. "
        "NOT a production penetration testing tool."
    ),
    version="1.0.0",
    docs_url="/docs",        # Swagger UI — great for judge demos
    redoc_url="/redoc",      # Alternative API docs
)


# ─── CORS Configuration ───────────────────────────────────────────────────────
# Allows local dev and deployed cloud frontends (Vercel, Render, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Wildcard origins require allow_credentials=False in standard CORS specs
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Startup Event ────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Initialize database, seed demo data, and optionally start simulated target app."""
    init_db()
    # Auto-seed if database is empty
    try:
        from backend.seed import seed_database
        seed_database()
    except Exception as e:
        print(f"Seed warning: {e}")

    # Launch local simulated target app on port 5001 in background thread
    # This enables live active scanning even on cloud platforms (Render, Railway, etc.)
    import threading
    def _run_target():
        try:
            from target_app.app import app as target_flask_app
            target_flask_app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
        except Exception as err:
            print(f"Target app background thread: {err}")

    t = threading.Thread(target=_run_target, daemon=True)
    t.start()
    print("Simulated World Monitor target app initialized on port 5001 (daemon thread).")


# ─── Routers ─────────────────────────────────────────────────────────────────
app.include_router(findings_router)
app.include_router(assessment_router)
app.include_router(report_router)


# ─── Static Frontend Serving (Self-Contained Full-Stack Deployment) ────────────
# When deployed to Render (e.g. https://sih26163.onrender.com),
# the dashboard UI is served directly from root /, while /api remains REST.
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
FRONTEND_ASSETS = os.path.join(FRONTEND_DIST, "assets")

if os.path.exists(FRONTEND_ASSETS):
    app.mount("/assets", StaticFiles(directory=FRONTEND_ASSETS), name="static-assets")

@app.get("/api")
def api_root():
    """API metadata endpoint."""
    return {
        "name": "SIH26163 Security Assessment API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
        "dashboard": "/api/dashboard",
        "findings": "/api/findings",
        "note": "Prototype — for Smart India Hackathon 2026 demonstration only.",
    }

@app.get("/{full_path:path}")
async def serve_frontend_spa(full_path: str):
    """
    Serves the React single-page application.
    If the requested path matches an actual static file in dist, return it.
    Otherwise, return index.html to allow client-side React routing.
    """
    if os.path.exists(FRONTEND_DIST):
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_file = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)

    # Fallback to API info if frontend is not built
    return {
        "name": "SIH26163 Security Assessment API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
        "dashboard": "/api/dashboard",
        "findings": "/api/findings",
    }


# ─── Run directly (alternative to uvicorn CLI) ────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
