from __future__ import annotations
import json
from phase1.models import RestaurantRecord
from phase2.models import UserPreferences

SYSTEM_PROMPT = """You are an elite food critic and personal concierge for Zomato. 
Your goal is to provide sophisticated, personalized restaurant recommendations based on a set of candidates.

### Constraints:
1. **Source Fidelity**: ONLY recommend restaurants from the provided candidate list. Use their exact 'id'.
2. **Personalization**: Tailor your justifications to the user's specific budget, cuisine, and 'extra' notes.
3. **Structured Output**: You must return a JSON object with a specific schema.

### JSON Output Schema:
{
  "summary": "A 1-sentence overview of the recommendations.",
  "rankings": [
    {
      "id": "string (the restaurant id)",
      "rank": "integer",
      "explanation": "A 1-2 sentence justification for this choice."
    }
  ]
}

### Reasoning Guidelines:
- If the user mentioned "date night," look for restaurants with appropriate rest_types or vibes.
- If the user has a "low" budget, highlight value-for-money.
- Be punchy and professional. Do not use generic filler words.
"""

def build_user_prompt(prefs: UserPreferences, candidates: list[RestaurantRecord]) -> str:
    # Convert candidates to a compact JSON string for the prompt
    candidate_data = [
        {
            "id": c.id,
            "name": c.name,
            "cuisines": c.cuisines,
            "rating": c.rating,
            "cost_for_two": c.cost_for_two_inr,
            "location": c.location,
            "type": c.rest_type
        }
        for c in candidates
    ]
    
    prompt = f"""### User Preferences:
{json.dumps(prefs.to_json_dict(), indent=2)}

### Candidates (JSON):
{json.dumps(candidate_data, indent=2)}

Please provide your ranked recommendations now."""
    return prompt
