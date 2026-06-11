import { useState, useEffect } from 'react';
import './index.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

function App() {
  const [locations, setLocations] = useState([]);
  const [loadingLocations, setLoadingLocations] = useState(true);
  const [formData, setFormData] = useState({ location: '', budget: '', cuisine: '', min_rating: 4.0, extra: '' });
  const [cuisinesList, setCuisinesList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMeta = async () => {
      try {
        const [locRes, cuiRes] = await Promise.all([
          fetch(`${API_URL}/meta/locations`),
          fetch(`${API_URL}/meta/cuisines`)
        ]);
        if (locRes.ok) setLocations(await locRes.json());
        if (cuiRes.ok) setCuisinesList(await cuiRes.json());
      } catch (err) {
        console.error(err);
      } finally {
        setLoadingLocations(false);
      }
    };
    fetchMeta();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.location) return setError('Location is required');
    
    setLoading(true);
    setError(null);
    setResults(null);

    let budgetToken = "high";
    if (formData.budget) {
      const b = parseInt(formData.budget);
      if (b <= 600) budgetToken = "low";
      else if (b <= 1500) budgetToken = "medium";
    }

    try {
      const res = await fetch(`${API_URL}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          budget: formData.budget ? budgetToken : "high",
          min_rating: parseFloat(formData.min_rating)
        })
      });

      if (!res.ok) throw new Error((await res.json()).detail || 'Failed to fetch');
      setResults(await res.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Background ambient glows */}
      <div className="ambient-glow glow-red"></div>
      <div className="ambient-glow glow-yellow"></div>

      <div className="hero">
        <div className="hero-content">
          <h1>AI Restaurant<br />Recommendation</h1>
          <p>Discover your next great meal with intelligent recommendations.</p>
        </div>
      </div>

      <form className="glass-panel search-container" onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="input-group">
            <label>Location <span className="required">*</span></label>
            <select name="location" value={formData.location} onChange={handleChange} required>
              <option value="" disabled>Select a neighborhood...</option>
              {locations.map(loc => <option key={loc} value={loc}>{loc}</option>)}
            </select>
          </div>

          <div className="input-group">
            <label>Cuisine</label>
            <select name="cuisine" value={formData.cuisine} onChange={handleChange}>
              <option value="">Any Cuisine</option>
              {cuisinesList.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div className="input-group">
            <label>Max Budget (for two)</label>
            <input type="number" name="budget" value={formData.budget} onChange={handleChange} placeholder="₹1500" min="0" step="100" />
          </div>

          <div className="input-group">
            <label>Minimum Rating</label>
            <select name="min_rating" value={formData.min_rating} onChange={handleChange}>
              <option value="0">Any</option>
              <option value="3.5">3.5 & Up</option>
              <option value="4.0">4.0 & Up</option>
              <option value="4.5">4.5 & Up</option>
            </select>
          </div>
        </div>

        <div className="input-group full-width">
          <label>Describe your perfect meal (Vibe, mood or specific cravings, date etc.)</label>
          <textarea name="extra" value={formData.extra} onChange={handleChange} placeholder="e.g. A quiet rooftop for a date, or live music and great momos..." rows="2" />
        </div>

        <button type="submit" className="glow-btn" disabled={loading}>
          {loading ? <span className="spinner"></span> : 'Find Restaurants'}
        </button>
      </form>

      {error && <div className="glass-panel error-message">{error}</div>}

      {loading && (
        <div className="results-container">
          <div className="cards-grid">
            {[1, 2, 3].map(i => (
              <div key={i} className="glass-panel skeleton-card">
                <div className="shimmer skeleton-title"></div>
                <div className="shimmer skeleton-meta"></div>
                <div className="shimmer skeleton-text"></div>
                <div className="shimmer skeleton-text"></div>
              </div>
            ))}
          </div>
        </div>
      )}

      {results && !loading && (
        <div className="results-container slide-up">
          <h2 className="results-header">Your Recommendations</h2>
          {results.summary && <div className="glass-panel results-summary">{results.summary}</div>}
          
          <div className="cards-grid">
            {results.recommendations.map((rec, idx) => (
              <div key={rec.restaurant.id} className="glass-panel result-card" style={{ animationDelay: `${idx * 0.1}s` }}>
                <div className="card-header">
                  <div className="rank-badge">#{rec.rank}</div>
                  <h3>{rec.restaurant.name}</h3>
                  <div className="meta-tags">
                    <span className="tag rating">★ {rec.restaurant.rating}</span>
                    <span className="tag price">₹{rec.restaurant.cost_for_two}</span>
                  </div>
                  <p className="cuisines">{rec.restaurant.cuisines}</p>
                </div>
                <div className="card-body">
                  <p className="explanation">"{rec.explanation}"</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
