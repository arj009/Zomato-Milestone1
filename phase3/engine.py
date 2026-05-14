from __future__ import annotations
import json
import logging
import os
from pathlib import Path
from typing import Optional, Sequence
from groq import Groq
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env from the current directory (phase3) or project root
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from phase1.models import RestaurantRecord
from phase2.models import UserPreferences
from phase3.models import EngineResult, RankedRecommendation
from phase3.prompt import SYSTEM_PROMPT, build_user_prompt

def run_recommendation_engine(
    prefs: UserPreferences,
    shortlisted: list[RestaurantRecord],
    api_key: Optional[str] = None
) -> EngineResult:
    """
    Orchestrates the LLM recommendation flow using Groq. 
    Falls back to deterministic ranking if LLM fails.
    """
    if not shortlisted:
        return EngineResult(summary="No restaurants matched your criteria.", recommendations=[], source="fallback")

    # Use provided key or environment variable
    key = api_key or os.getenv("GROQ_API_KEY")
    
    if not key:
        logger.warning("GROQ_API_KEY not found. Falling back to deterministic rankings.")
        return _deterministic_fallback(shortlisted, "API key missing. Using database rankings.")

    try:
        # 1. Initialize Groq Client
        client = Groq(api_key=key)
        
        # 2. Build Prompts
        user_prompt = build_user_prompt(prefs, shortlisted)
        
        # 3. Call Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        # 4. Parse Response
        response_text = chat_completion.choices[0].message.content
        data = json.loads(response_text)
        summary = data.get("summary")
        rankings_raw = data.get("rankings", [])
        
        # 5. Map back to RestaurantRecords
        by_id = {r.id: r for r in shortlisted}
        recommendations = []
        seen_ids = set()
        
        for item in rankings_raw:
            rid = item.get("id")
            if rid in by_id and rid not in seen_ids:
                recommendations.append(RankedRecommendation(
                    rank=len(recommendations) + 1,
                    record=by_id[rid],
                    explanation=item.get("explanation", "Highly recommended based on your preferences.")
                ))
                seen_ids.add(rid)
        
        # Fill in any missing ones from the shortlist if the LLM missed them
        for r in shortlisted:
            if r.id not in seen_ids:
                recommendations.append(RankedRecommendation(
                    rank=len(recommendations) + 1,
                    record=r,
                    explanation="Recommended based on high ratings and budget match."
                ))
        
        return EngineResult(summary=summary, recommendations=recommendations, source="groq")

    except Exception as e:
        logger.error(f"Groq Engine failed: {e}")
        return _deterministic_fallback(shortlisted, f"Groq error: {str(e)}")

def _deterministic_fallback(shortlisted: list[RestaurantRecord], error_note: str) -> EngineResult:
    recs = [
        RankedRecommendation(rank=i+1, record=r, explanation="Top-rated option in your requested area.")
        for i, r in enumerate(shortlisted)
    ]
    return EngineResult(
        summary="Here are the top-rated restaurants matching your criteria.",
        recommendations=recs,
        source="fallback",
        error_note=error_note
    )
