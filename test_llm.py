from phase1.catalog import load_catalog_jsonl
from phase2.build import build_user_preferences
from phase2.filter import filter_catalog
from phase2.shortlist import shortlist_candidates
from phase3.engine import run_recommendation_engine

def main():
    CATALOG_PATH = "data/catalog.jsonl"
    
    print("Testing Phase 3: Live Recommendation Engine")
    
    # 1. Setup Data
    catalog = load_catalog_jsonl(CATALOG_PATH)
    
    # Input from User Request: Bellandur, Budget 2000, Rating 4.0
    raw_input = {
        "location": "Bellandur",
        "budget": "high", # 2000 maps to High (>800)
        "cuisine": "",    # Not specified
        "min_rating": 4.0,
        "extra": ""
    }
    
    try:
        # 2. Logic Layer (Phase 2)
        prefs = build_user_preferences(**raw_input)
        candidates = filter_catalog(catalog, prefs)
        shortlist = shortlist_candidates(candidates, max_n=5) # Get top 5
        
        print(f"Preferences: {prefs}")
        print(f"Shortlisted Candidates: {len(shortlist)}")
        
        # 3. LLM Layer (Phase 3)
        result = run_recommendation_engine(prefs, shortlist)
        
        print(f"Engine Source: {result.source}")
        if result.error_note:
            print(f"Note: {result.error_note}")
            
        print(f"\nSummary: {result.summary}")
        print("-" * 50)
        for rec in result.recommendations:
            print(f"Rank {rec.rank}: {rec.record.name}")
            print(f"Rating: {rec.record.rating} | Cost: {rec.record.cost_for_two_inr} | Cuisine: {rec.record.cuisines}")
            print(f"AI Reasoning: {rec.explanation}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    main()
