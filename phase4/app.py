import logging
import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from phase1.catalog import load_catalog_jsonl
from phase2.build import build_user_preferences
from phase2.filter import filter_catalog
from phase2.shortlist import shortlist_candidates
from phase3.engine import run_recommendation_engine
from phase4.api_models import RecommendRequest, EngineResponse, RecommendationResponse, RestaurantInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use absolute path for catalog to ensure it works on Render
BASE_DIR = Path(__file__).parent.parent
CATALOG_PATH = os.getenv("CATALOG_PATH", str(BASE_DIR / "data" / "catalog.jsonl"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load catalog on startup
    logger.info("Loading catalog from %s...", CATALOG_PATH)
    try:
        app.state.catalog = load_catalog_jsonl(CATALOG_PATH)
        logger.info("Catalog loaded: %s records.", len(app.state.catalog.records))
    except Exception as e:
        logger.error("Failed to load catalog: %s", e)
        app.state.catalog = None
    yield

app = FastAPI(title="Zomato AI Recommendation API", lifespan=lifespan)

# Enable CORS for frontend integration
# Read allowed origins from env var, defaulting to all for development.
# In production (Render), set ALLOWED_ORIGINS to your Vercel URL.
allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [o.strip() for o in allowed_origins_raw.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "catalog_loaded": app.state.catalog is not None}

@app.get("/locations")
@app.get("/meta/locations")
def get_locations():
    if not app.state.catalog:
        return []
    # Get unique locations from the catalog
    locations = sorted(list(set(r.location for r in app.state.catalog.records if r.location)))
    return locations

@app.get("/meta/cuisines")
def get_cuisines():
    if not app.state.catalog:
        return []
    cuisines_set = set()
    for r in app.state.catalog.records:
        if r.cuisines:
            for c in r.cuisines.split(","):
                c = c.strip()
                if c:
                    cuisines_set.add(c)
    # Return top 50 or so, or just all sorted
    return sorted(list(cuisines_set))

@app.post("/recommend", response_model=EngineResponse)
async def recommend(req: RecommendRequest):
    if not app.state.catalog:
        raise HTTPException(status_code=503, detail="Catalog not loaded")

    try:
        # 1. Build and Validate Preferences
        prefs = build_user_preferences(
            location=req.location,
            budget=req.budget,
            cuisine=req.cuisine or "",
            min_rating=req.min_rating,
            extra=req.extra or ""
        )
        
        # 2. Filtering Logic (Phase 2)
        candidates = filter_catalog(app.state.catalog, prefs)
        print(f">>> [API] Found {len(candidates)} candidates after filtering.")
        
        if not candidates:
             print(">>> [API] No candidates found. Returning early.")
             return EngineResponse(
                summary="No restaurants matched your specific criteria. Try broadening your search!",
                recommendations=[],
                source="filter"
            )

        # 3. Shortlisting (Top 10 for the LLM)
        shortlist = shortlist_candidates(candidates, max_n=10)
        print(f">>> [API] Shortlisted {len(shortlist)} candidates for LLM.")
        
        # 4. LLM Orchestration (Phase 3)
        result = run_recommendation_engine(prefs, shortlist)
        print(f">>> [API] Recommendation source: {result.source}")
        
        # 5. Format Response
        recs = [
            RecommendationResponse(
                rank=r.rank,
                explanation=r.explanation,
                restaurant=RestaurantInfo(
                    id=r.record.id,
                    name=r.record.name,
                    location=r.record.location,
                    rating=r.record.rating,
                    cost_for_two=r.record.cost_for_two_inr,
                    cuisines=r.record.cuisines,
                    rest_type=r.record.rest_type
                )
            )
            for r in result.recommendations
        ]
        
        return EngineResponse(
            summary=result.summary or "Top picks for you",
            recommendations=recs,
            source=result.source
        )

    except Exception as e:
        logger.error("Recommendation failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
