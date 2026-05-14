from phase1.catalog import load_catalog_jsonl
from phase2.build import build_user_preferences
from phase2.filter import filter_catalog
from phase2.shortlist import shortlist_candidates

def main():
    CATALOG_PATH = "data/catalog.jsonl"
    
    print("Testing Phase 2: Logic Layer...")
    
    # 1. Load the catalog built in Phase 1
    catalog = load_catalog_jsonl(CATALOG_PATH)
    
    # 2. Simulate User Input
    raw_input = {
        "location": "Banashankari", # Using a known location from the catalog snippet I saw
        "budget": "medium",
        "cuisine": "Cafe",
        "min_rating": 4.0,
        "extra": "Italian"
    }
    
    try:
        # 3. Build and Validate Preferences
        prefs = build_user_preferences(**raw_input)
        print(f"Preferences validated: {prefs}")
        
        # 4. Filter Catalog
        candidates = filter_catalog(catalog, prefs)
        print(f"Candidates found: {len(candidates)}")
        
        # 5. Shortlist
        top_picks = shortlist_candidates(candidates, max_n=5)
        print(f"Top {len(top_picks)} Picks:")
        for i, r in enumerate(top_picks, 1):
            print(f"  {i}. {r.name} ({r.rating} stars, {r.cost_for_two_inr} INR) - {r.location}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
