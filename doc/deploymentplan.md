# Deployment Plan: Zomato AI Recommendation System

This plan details the steps to deploy the application with the **Backend on Render** and the **Frontend on Vercel**.

## 1. Backend Deployment (Render)

Render is ideal for hosting the FastAPI backend.

### Prerequisites
- A [Render](https://render.com/) account connected to your GitHub/GitLab repository.
- Ensure `requirements.txt` exists in the root (created).
- The `data/catalog.jsonl` file must be included in your repository.

### Steps
1. **Create a New Web Service:**
   - In the Render dashboard, click **New** > **Web Service**.
   - Select your repository.
2. **Configure Service Settings:**
   - **Name:** `zomato-ai-backend` (or your preferred name)
   - **Language:** `Python 3`
   - **Branch:** `main` (or your default branch)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn phase4.app:app --host 0.0.0.0 --port $PORT`
3. **Set Environment Variables:**
   - Go to the **Environment** tab.
   - Add `GROQ_API_KEY`: Paste your Groq API key here.
4. **Deploy:**
   - Render will build and deploy your service.
   - **Copy the service URL** (e.g., `https://zomato-ai-backend.onrender.com`). You will need this for the frontend.

---

## 2. Frontend Deployment (Vercel)

Vercel is optimized for React/Vite applications.

### Prerequisites
- A [Vercel](https://vercel.com/) account.
- The Render backend URL from the previous step.

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
   - Add `VITE_API_URL`: Paste your Render backend URL (e.g., `https://zomato-ai-backend.onrender.com`).
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
The backend in `phase4/app.py` is currently configured to allow all origins (`allow_origins=["*"]`). While this works for testing, for better security in production, you should eventually restrict it to your Vercel URL.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.vercel.app", "http://localhost:5173"],
    # ...
)
```

---

## Deployment Checklist
- [ ] Backend deployed to Render?
- [ ] `GROQ_API_KEY` set in Render?
- [ ] Frontend deployed to Vercel?
- [ ] `VITE_API_URL` set in Vercel pointing to Render?
- [ ] Test the live Vercel URL for recommendations.
