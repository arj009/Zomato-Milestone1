# Migration Plan: Railway to Render

This plan outlines the steps to migrate the Python backend to Render without disturbing the existing Railway deployment, ensuring zero downtime.

## 1. Prerequisites
- Create a free account on [Render.com](https://render.com/).
- Ensure your GitHub account is linked to Render so you can deploy from your repository.

## 2. Setup Render Web Service
1. In the Render Dashboard, click **New** and select **Web Service**.
2. Connect the `ZomatoMilestone1` repository.
3. Configure the service settings:
   - **Name**: `zomato-ai-backend` (or any preferred name)
   - **Region**: Select the region closest to your Vercel frontend.
   - **Branch**: `main` (or whichever branch you are using).
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn phase4.app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

*Note: Your `Procfile` is already configured for Railway (`web: uvicorn phase4.app:app --host 0.0.0.0 --port ${PORT:-8001}`). Render supports Procfiles automatically, but defining the Build/Start commands explicitly ensures it runs correctly.*

## 3. Configure Environment Variables
Copy over the necessary environment variables from your Railway dashboard to Render.
1. In the Render Web Service settings, go to the **Environment** tab.
2. Add all secrets used in your application (e.g., `OPENAI_API_KEY`, or any database URLs).
3. *Note:* Render automatically provides the `PORT` environment variable.

## 4. Deploy and Verify
1. Click **Create Web Service**. Render will automatically start the build process.
2. Monitor the build logs to ensure dependencies in `requirements.txt` install successfully.
3. Once deployed, Render will provide a URL (e.g., `https://zomato-ai-backend-xxxx.onrender.com`).
4. Test the new Render URL directly (e.g., via Postman, curl, or your browser) to ensure the API responds correctly.

## 5. Update Frontend Configuration
Once the Render backend is verified and running:
1. Go to your Vercel Dashboard (where your frontend is hosted).
2. Open the project settings and navigate to **Environment Variables**.
3. Update the backend URL variable (e.g., `VITE_API_URL`, `NEXT_PUBLIC_API_URL`, or `REACT_APP_API_URL`) from the current Railway URL to the new Render URL.
4. Redeploy your frontend on Vercel so the changes take effect.

## 6. Teardown Railway Deployment
Now that Render is fully operational and the frontend is successfully communicating with it, you can safely remove your backend from Railway to avoid any future billing or resource usage:

1. Log in to your [Railway Dashboard](https://railway.app/dashboard).
2. Click on your `ZomatoMilestone1` project.
3. **Delete the Service**: 
   - Click on the specific backend service inside the project.
   - Go to the **Settings** tab.
   - Scroll all the way to the bottom to the **Danger Zone**.
   - Click **Delete Service** and confirm.
4. **Delete the Project (Optional but recommended)**:
   - Go back to the main project view.
   - Click on the **Project Settings** (gear icon) in the top right.
   - Scroll down to the bottom and click **Delete Project**.
   - Type the project name to confirm deletion.

Congratulations on the successful migration!
