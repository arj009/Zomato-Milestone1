# Deployment Plan: Zomato AI Recommendation System

This plan details the steps to deploy the application with the **Backend on Railway** and the **Frontend on Vercel**.

## 1. Backend Deployment (Railway)

Railway is excellent for hosting FastAPI backends with minimal configuration.

### Prerequisites
- A [Railway](https://railway.app/) account.
- Ensure `requirements.txt` exists in the root (created).
- The `Procfile` exists in the root (created).
- The `data/catalog.jsonl` file must be included in your repository.

### Steps
1. **Create a New Project:**
   - In the Railway dashboard, click **New Project** > **Deploy from GitHub repo**.
   - Select your repository.
2. **Configure Service Settings:**
   - Railway will automatically detect the `Procfile` and use it for the start command.
   - **Start Command (from Procfile):** `uvicorn phase4.app:app --host 0.0.0.0 --port ${PORT:-8001}`
3. **Set Environment Variables:**
   - Go to the **Variables** tab in your Railway service.
   - Add `GROQ_API_KEY`: Paste your Groq API key here.
   - Add `GROQ_MODEL`: (Optional) `llama-3.3-70b-versatile`.
4. **Deploy:**
   - Railway will build and deploy your service automatically.
   - **Copy the service URL** (e.g., `https://zomato-ai-backend-production.up.railway.app`). You will need this for the frontend.

---

## 2. Frontend Deployment (Vercel)

Vercel is optimized for React/Vite applications.

### Prerequisites
- A [Vercel](https://vercel.com/) account.
- The Railway backend URL from the previous step.

### Steps
1. **Import Project:**
   - In the Vercel dashboard, click **Add New** > **Project**.
   - Import your repository.
2. **Configure Project Settings:**
   - **Framework Preset:** `Vite` (automatically detected).
   - **Root Directory:** Select the `frontend` folder.
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. **Set Environment Variables:**
   - Add `VITE_API_URL`: Paste your Railway backend URL (e.g., `https://zomato-ai-backend.up.railway.app`).
4. **Deploy:**
   - Click **Deploy**. Vercel will build the frontend.
5. **Verify:**
   - Visit the provided Vercel URL (e.g., `https://zomato-ai-frontend.vercel.app`).

---

## 3. Important Code Adjustments

### Update API Endpoint in Frontend
Ensure the frontend uses the environment variable for the API URL.
In `frontend/src/App.jsx`, update the `API_URL` constant:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
```

### CORS Configuration in Backend
The backend in `phase4/app.py` is configured to allow origins via the `ALLOWED_ORIGINS` environment variable.

```python
# Set this variable in Railway dashboard
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:5173
```

---

## Deployment Checklist
- [ ] Backend deployed to Railway?
- [ ] `GROQ_API_KEY` set in Railway?
- [ ] Frontend deployed to Vercel?
- [ ] `VITE_API_URL` set in Vercel pointing to Railway?
- [ ] Test the live Vercel URL for recommendations.
