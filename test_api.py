import requests
import time

BASE_URL = "http://localhost:8001"

def test_endpoint(name, method, path, payload=None):
    print(f"\n--- Testing {name} ---")
    start_time = time.time()
    try:
        if method == "GET":
            resp = requests.get(f"{BASE_URL}{path}")
        else:
            resp = requests.post(f"{BASE_URL}{path}", json=payload)
        
        duration = time.time() - start_time
        print(f"Status: {resp.status_code}")
        print(f"Time: {duration:.2f}s")
        
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Error: {resp.text}")
            return None
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def run_all_tests():
    print("Starting Phase 4 API Tests...")

    # 1. Health Check
    health = test_endpoint("Health Check", "GET", "/health")
    if health:
        print(f"Server Status: {health['status']}")

    # 2. Meta Locations (New Endpoint)
    locations = test_endpoint("Meta Locations", "GET", "/meta/locations")
    if locations:
        print(f"Found {len(locations)} locations.")
        print(f"Sample: {locations[:5]}")

    # 3. Valid Recommendation
    payload = {
        "location": "Bellandur",
        "budget": "high",
        "min_rating": 4.0,
        "cuisine": "North Indian"
    }
    recs = test_endpoint("Valid Recommendation (North Indian in Bellandur)", "POST", "/recommend", payload)
    if recs:
        print(f"Summary: {recs['summary']}")
        print(f"Source: {recs['source']}")
        if recs['recommendations']:
            top = recs['recommendations'][0]['restaurant']
            print(f"Top Pick: {top['name']} ({top['rating']}⭐)")

    # 4. No Matches Scenario
    payload = {
        "location": "Bellandur",
        "budget": "low",
        "min_rating": 5.0, # Highly unlikely to find many 5.0 in low budget
        "cuisine": "Icelandic" # Non-existent cuisine
    }
    no_recs = test_endpoint("No Matches (Icelandic in Bellandur)", "POST", "/recommend", payload)
    if no_recs:
        print(f"Expected Empty Result: {no_recs['summary']}")

    # 5. Invalid Location
    payload = {
        "location": "Mars",
        "budget": "medium"
    }
    invalid_loc = test_endpoint("Invalid Location (Mars)", "POST", "/recommend", payload)
    if invalid_loc:
        print(f"Response: {invalid_loc['summary']}")

    print("\n✅ All tests completed.")

if __name__ == "__main__":
    run_all_tests()
