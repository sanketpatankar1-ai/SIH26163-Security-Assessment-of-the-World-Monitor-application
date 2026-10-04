@echo off
TITLE World Monitor Security Assessment Platform - Launcher
echo ========================================================
echo   SIH26163 - World Monitor Security Assessment Platform
echo ========================================================
echo.

echo [1/3] Starting Simulated World Monitor Target App (Port 5001)...
start "World Monitor Target App (Port 5001)" cmd /k ".venv\Scripts\python target_app\app.py"

timeout /t 2 /nobreak >nul

echo [2/3] Starting FastAPI Backend (Port 8000)...
start "FastAPI Backend (Port 8000)" cmd /k ".venv\Scripts\uvicorn backend.main:app --reload --port 8000"

timeout /t 2 /nobreak >nul

echo [3/3] Starting React Vite Frontend (Port 5173)...
start "React Frontend (Port 5173)" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================================
echo   All 3 services are launching:
echo   - Target App: http://localhost:5001
echo   - API Swagger Docs: http://localhost:8000/docs
echo   - Security Dashboard: http://localhost:5173
echo ========================================================
echo.
echo Opening Dashboard in your browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:5173
