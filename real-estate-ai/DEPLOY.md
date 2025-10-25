# Deploy Real Estate AI

This guide shows two production deployment paths:

- Option A: Docker Compose with Nginx (one host, simple and reliable)
- Option B: Managed services (frontend on Netlify/Cloudflare, backend on Render/Railway, DB on MongoDB Atlas)

Both assume Windows PowerShell for local commands.

---

## Option A — Docker Compose (Nginx reverse proxy)

What you get:
- Backend (FastAPI + Uvicorn) on an internal container
- Frontend (React build) served by Nginx
- Nginx proxies `/api` to the backend, so no CORS in production

### 1) Prerequisites
- Docker Desktop installed (Windows/Mac) and running
- A MongoDB instance (recommended: MongoDB Atlas)
- A strong JWT secret

### 2) Configure backend env
Create `real-estate-ai/backend/.env` from the template:

```
Copy-Item real-estate-ai/backend/.env.example real-estate-ai/backend/.env
notepad real-estate-ai/backend/.env
```

Fill in at least:
- MONGODB_URL=mongodb connection string
- DATABASE_NAME=realestate_srilanka
- JWT_SECRET=your-strong-secret
- ALLOW_ORIGINS=http://localhost:8080,https://your-domain.com
- GEMINI_API_KEY= (optional)
- STRIPE_* (optional)

### 3) Build and run
From the `real-estate-ai` folder:

```powershell
cd real-estate-ai
# First build images
docker compose build
# Then start containers
docker compose up -d
```

- Frontend: http://localhost:8080
- API via Nginx: http://localhost:8080/api
- Backend container (internal): http://backend:8000 (inside the docker network)

Logs:
```powershell
docker compose logs -f backend
# or
docker compose logs -f web
```

Stop:
```powershell
docker compose down
```

### 4) Deploying to a VM/server
- Copy the `real-estate-ai/` folder to your VM
- Set `backend/.env` with your production values
- Run the same `docker compose build` and `docker compose up -d`
- Point your DNS to the server
- Optionally put a TLS-terminating reverse proxy (e.g., Caddy/Traefik) in front of the `web` service for HTTPS

Note: The backend image installs heavy ML dependencies (transformers, faiss, spacy). Build time and RAM usage can be significant; choose a machine with at least 4–8 GB RAM.

---

## Option B — Managed services

### Overview
- Database: MongoDB Atlas (recommended)
- Backend: Render or Railway (build from repo)
- Frontend: Netlify, Cloudflare Pages, or Vercel (static site)

### 1) MongoDB Atlas
- Create a free/shared cluster
- Create a database user and get the connection string (SRV URI)
- Whitelist your server/IP (or 0.0.0.0/0 for testing only)

### 2) Backend on Render (example)
- Create a new Web Service from your GitHub repo in Render
- Runtime: Python 3.11
- Build command:
  - `pip install -r real-estate-ai/backend/requirements.txt`
- Start command:
  - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Root directory: `real-estate-ai/backend`
- Add environment variables in Render dashboard (match backend/.env.example):
  - MONGODB_URL, DATABASE_NAME, JWT_SECRET, ALLOW_ORIGINS, GEMINI_API_KEY, STRIPE_*
- Once deployed, note the public URL, e.g. `https://your-backend.onrender.com`

### 3) Frontend on Netlify or Cloudflare Pages
- Build command: `npm run build`
- Publish directory: `real-estate-ai/frontend/dist`
- Root directory: `real-estate-ai/frontend`
- Set an environment variable for the API base URL:
  - `VITE_API_BASE_URL=https://your-backend.onrender.com`
- Re-deploy. The app will call the backend directly.

If you prefer to keep the `/api` path, you can configure a redirect/proxy rule in Netlify/Cloudflare to forward `/api/*` to your backend.

---

## CORS and Auth tokens
- In Option A (Compose), the browser hits the same origin (`localhost:8080`) and Nginx proxies `/api` → no CORS needed.
- In Option B (different domains), set `ALLOW_ORIGINS` in backend `.env` to include your frontend domain(s).
- Authentication uses a JWT in `localStorage`. Ensure you serve over HTTPS in production.

---

## Security checklist
- Never commit real secrets (JWT, DB URI, API keys). Rotate any that were exposed.
- Use unique, strong `JWT_SECRET` per environment.
- Limit MongoDB network access using IP allowlists and strong user passwords.
- Add HTTPS via your hosting provider or a proxy (Caddy/Traefik/NGINX with certs).

---

## Troubleshooting
- 401s after deploy: confirm `ALLOW_ORIGINS` and that your frontend uses the correct `VITE_API_BASE_URL`.
- Long/timeout requests: the Nginx config raises timeouts to 120s; ensure your host/Load Balancer also allows longer timeouts.
- Backend cannot connect to DB: verify `MONGODB_URL` and networking (Atlas IP allowlist, firewalls, etc.).
- Large container builds: use a machine with adequate RAM; builds may take several minutes due to ML libraries.
