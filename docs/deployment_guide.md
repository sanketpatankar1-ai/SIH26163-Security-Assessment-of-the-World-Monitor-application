# Cloud Deployment Guide — SIH26163 Security Platform

This guide walks you through deploying the **SIH26163 Security Assessment Platform** to free cloud hosting using **Render (Backend)** and **Vercel (Frontend)**.

---

## Part 1: Deploy Backend on Render (Free Tier)

Render hosts the FastAPI backend server, SQLite database, ReportLab PDF generator, and background simulated target app.

### Step-by-Step:
1. Go to [render.com](https://render.com) and log in with your GitHub account.
2. Click **"New +"** in the dashboard and select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and select your repo:
   `https://github.com/Ozair-aly/SIH26163`
4. Fill in the following settings:
   - **Name:** `sih26163-backend` (or your preferred name)
   - **Region:** Any (e.g., Singapore or Frankfurt)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`
5. Click **"Create Web Service"**.
6. Once deployed, Render will provide a public URL like:
   `https://sih26163-backend.onrender.com`
   *(Copy this URL — you'll need it for the frontend).*

---

## Part 2: Deploy Frontend on Vercel (Free Tier)

Vercel provides lightning-fast global CDN edge hosting for the React 18 dashboard.

### Step-by-Step:
1. Go to [vercel.com](https://vercel.com) and sign in with your GitHub account.
2. Click **"Add New..."** → **"Project"**.
3. Import your repository: `Ozair-aly/SIH26163`.
4. Configure Project Settings:
   - **Framework Preset:** `Vite`
   - **Root Directory:** Click "Edit" and choose `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add the Environment Variable:
   - Click **"Environment Variables"**
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** `https://sih26163-backend.onrender.com` *(your Render backend URL from Part 1)*
6. Click **"Deploy"**.
7. In ~30 seconds, your site will be live at:
   `https://sih26163.vercel.app`

---

## Part 3: Verification Checklist

Once both services are deployed:
- [ ] Open your Vercel URL in your browser.
- [ ] Verify the **Security Scorecard** loads (e.g., 78/100, Grade B).
- [ ] Click **"Run Assessment"** to trigger a live cloud scan.
- [ ] Click on a finding to inspect evidence and change status to **"Fixed"** (verify dynamic score recovery).
- [ ] Click **"Download Report"** to test live cloud PDF generation.
