# LinkedIn Post — Zomato AI Recommendation Engine

---

## ✍️ Post (Copy & Paste Ready)

---

Most search boxes don't understand you.

You type *"good Italian restaurant in Bangalore under ₹1000"* — and you get a list sorted by rating. 
That's not a recommendation. That's a spreadsheet.

I set out to fix that. Here's how I built an AI-powered restaurant discovery engine from scratch — and what I learned about building AI products along the way. 🧵

---

**🎯 The Problem I Started With**

The traditional search-and-filter UX is broken for food discovery. Users don't just want options. They want a *reason* — the "why this place, for me, tonight."

No existing filter can answer: *"I want somewhere cozy, good for a date, with great pasta, not too pricey."*

That's not a filter problem. That's a reasoning problem. And LLMs are built for exactly this.

---

**🏗️ My PM Instinct: Phase Everything**

One of the biggest mistakes in AI product development is trying to build the full system in one shot. I resisted that temptation.

I broke this into **5 deliberate phases**, each with a single clear success metric:

**Phase 1 — Foundation (Data)**
Before any AI, I needed a source of truth.
→ Ingested the Zomato restaurant dataset from Hugging Face
→ Cleaned, normalized city names and price ranges
→ Built a lightweight local catalog for fast querying
*Success metric: Return a clean restaurant list for any city. Nothing more.*

**Phase 2 — Logic Layer (Smart Filtering)**
LLMs are expensive and have token limits. Don't throw 10,000 restaurants at a model.
→ Built deterministic hard filters: Location, Cuisine, Budget, Rating
→ Pre-ranked candidates by rating to select the best 10–15
→ Packaged them as compact JSON for the LLM
*Success metric: "Italian in Bangalore under ₹1000" returns ~10 clean candidates.*

**Phase 3 — Intelligence Layer (LLM Orchestration)**
This is where the magic happens — but only if the prompt is right.
→ System prompt: "You are a local food expert..." (role + constraints)
→ User prompt: Dynamic injection of preferences + candidate set
→ Instructed the model to explain *why* each restaurant fits the user's vibe
*Success metric: Unique, non-generic justifications. Not "highly rated." Something real.*

**Phase 4 — Backend Layer (FastAPI)**
AI without an API is just a script.
→ Built a FastAPI server with async processing
→ `POST /recommend` endpoint: preferences in → ranked AI picks out
→ Unified all 3 phases into a single service under 2 seconds
*Success metric: <2 second response. Production-ready.*

**Phase 5 — Experience Layer (React + Vite)**
Great AI deserves a great interface.
→ Result cards showing restaurant name, cuisine, rating, and AI justification
→ Loading states, error handling, empty states — the full UX polish
→ Deployed on Vercel + Railway for live access
*Success metric: A user can discover their next meal through a beautiful, responsive UI.*

---

**💡 The Key AI PM Insight That Changed Everything**

There's a phenomenon called **"Lost in the Middle"** — LLMs perform worst on information buried in long prompts.

The fix? Never pass more than 10 restaurants to the LLM.
Filter first. Reason second. This single architectural decision made the recommendations dramatically better AND cut latency in half.

Good AI products aren't just about the model. They're about what you put *around* the model.

---

**📦 What I Built**

✅ End-to-end recommendation pipeline: Data → Filter → LLM → API → UI
✅ Live deployment on Railway (backend) + Vercel (frontend)
✅ AI-generated, personalized justifications for every recommendation
✅ Clean, scalable 5-phase architecture — extensible for vector/semantic search

---

**What's Next?**
Phase 6 is about moving from hard filters to **semantic search** — so a user can type "date night vibes" and the system *understands*. Think embeddings, vector stores, vibe-matching.

The shift from keyword search → semantic search is the next frontier in consumer AI products. And I'm building toward it.

---

If you're learning AI Product Management or building with LLMs — the most important skill isn't prompt engineering.

It's **system thinking**. Knowing where the AI fits. And where it doesn't.

Happy to connect with anyone exploring this space. 🙌

**#AIProductManagement #LLM #GenerativeAI #MachineLearning #FastAPI #React #BuildInPublic #ProductManagement #AIEngineering #FoodTech**

---

## 📝 Notes for You

- **Hook**: Opens with a relatable pain point, not a tech pitch.
- **Storytelling arc**: Problem → Design thinking → Phase-by-phase build → Key insight → Future vision.
- **PM angle**: Each phase has a *success metric* — this signals product discipline, not just coding.
- **"Lost in the Middle"** insight is the "aha moment" — something non-obvious that makes you look sharp.
- **CTA**: Soft, no pressure, invites connection.
- You can add **1 image/carousel** of the architecture diagram from `PhaseWiseArchitecture.md` rendered as a graphic — it will boost reach significantly on LinkedIn.
