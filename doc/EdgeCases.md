# 🛡️ Edge Cases & Mitigation Strategy

This document identifies potential failure modes and edge cases for the Zomato AI Recommendation Engine, categorized by architectural phase.

---

## 📊 Phase 1: Data Ingestion & Catalog
*Focus: Ensuring a robust and clean "Source of Truth".*

| Edge Case | Risk | Mitigation Strategy |
| :--- | :--- | :--- |
| **Schema Drift** | HF dataset columns rename or vanish. | Implement a **Schema Validator** at ingestion; fail fast if critical columns (name, lat/long) are missing. |
| **Null Critical Fields** | Missing ratings or cost data. | Use **Default Imputation** (e.g., mark rating as 'N/A') or exclude rows with 0 critical info. |
| **Dirty Encodings** | Strange Unicode characters in names. | Apply **NFKC Normalization** and strip non-printable characters during ingestion. |
| **Duplicate Entries** | Same restaurant appearing multiple times. | Deduplicate based on a composite key: `(Name + Location + Address)`. |

---

## ⚙️ Phase 2: Logic & Filtering
*Focus: Handling the gap between user intent and available data.*

| Edge Case | Risk | Mitigation Strategy |
| :--- | :--- | :--- |
| **Zero Results** | "Sushi in a village" returns 0 matches. | **Graceful Fallback**: Suggest expanding the radius or trying a related cuisine (e.g., "Asian"). |
| **Conflicting Filters** | "Low Budget" + "Michelin Star". | **Constraint Relaxation**: Inform the user which filter is the "bottleneck" and suggest adjustments. |
| **Ambiguous Geography** | "Delhi" vs "New Delhi" vs "NCR". | Use a **Geographic Alias Table** or fuzzy matching (Levenshtein distance) for city names. |
| **Extreme Constraints** | Budget = 0 or Rating > 5. | **Input Validation**: Reject out-of-bounds values at the UI/API level with clear error messages. |

---

## 🧠 Phase 3: LLM Intelligence
*Focus: Mitigating non-deterministic and hallucination risks.*

| Edge Case | Risk | Mitigation Strategy |
| :--- | :--- | :--- |
| **Hallucination** | LLM recommends a restaurant NOT in the list. | **Context Post-Validation**: Cross-reference every LLM recommendation ID against the original shortlist. |
| **JSON Corruption** | LLM returns text instead of structured data. | Use **Pydantic Output Parsers** (LangChain) or a "JSON-Repair" utility pass. |
| **Prompt Injection** | User tries to "jailbreak" via free-text. | **Instruction Layering**: Use clear delimiters (`### Context ###`) and strict system prompts to ignore instruction overrides. |
| **Token Overflow** | Shortlist is too long for context window. | **Dynamic Truncation**: Calculate tokens before calling the LLM and cap the list to the top 10 candidates. |

---

## 📱 Phase 4: Experience & Performance
*Focus: Maintaining a premium user feel under stress.*

| Edge Case | Risk | Mitigation Strategy |
| :--- | :--- | :--- |
| **LLM Latency** | Response takes >10 seconds. | **Optimistic UI**: Show the filtered list immediately, then "stream" or "pop-in" the AI explanations. |
| **API Failure** | LLM key expires or service is down. | **Circuit Breaker**: Fall back to a standard deterministic list (Ranked by Rating) without AI commentary. |
| **Long Explanations** | AI writes a paragraph that breaks UI layout. | **Token Capping**: Force the LLM to provide explanations in <150 characters via the prompt. |
| **Accessibility** | Screen readers failing on AI text. | Ensure **Semantic HTML** and ARIA labels for AI-generated components. |

---

> [!IMPORTANT]
> **The Golden Rule of AI Recommendations**:
> Never trust the LLM with "Hard Facts" (Price, Rating, Address). Always pull these values directly from your **Phase 1 Catalog** and only use the LLM for **Ranking** and **Justification**.
