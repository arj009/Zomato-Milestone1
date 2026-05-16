import { useState, useEffect } from 'react';
import './index.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

function App() {
  const [locations, setLocations] = useState([]);
  const [loadingLocations, setLoadingLocations] = useState(true);
  
  const [formData, setFormData] = useState({
    location: '',
    budget: '',
    cuisine: '',
    min_rating: 4.0,
    extra: ''
  });

  const [cuisinesList, setCuisinesList] = useState([]);

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch locations for autocomplete
    const fetchLocations = async () => {
      try {
        const res = await fetch(`${API_URL}/meta/locations`);
        if (!res.ok) throw new Error('Failed to load locations');
        const data = await res.json();
        setLocations(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoadingLocations(false);
      }
    };
    const fetchCuisines = async () => {
      try {
        const res = await fetch(`${API_URL}/meta/cuisines`);
        if (!res.ok) throw new Error('Failed to load cuisines');
        const data = await res.json();
        setCuisinesList(data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchLocations();
    fetchCuisines();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.location) {
      setError('Location is required');
      return;
    }
    
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
          min_rating: parseFloat(formData.min_rating),
          extra: formData.extra
        })
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Failed to fetch recommendations');
      }

      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="hero">
        <header>
          <h1>Zomato AI Guide</h1>
          <p>Discover your next great meal with intelligent recommendations</p>
        </header>
      </div>

      <form className="search-container" onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="input-group">
            <label htmlFor="location">Where are you looking?</label>
            <select 
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
            >
              <option value="" disabled>Select a location...</option>
              {locations.map(loc => <option key={loc} value={loc}>{loc}</option>)}
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="cuisine">Craving anything specific?</label>
            <select 
              id="cuisine"
              name="cuisine"
              value={formData.cuisine}
              onChange={handleChange}
            >
              <option value="">Any Cuisine</option>
              {cuisinesList.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="budget">Max Budget (for two)</label>
            <input 
              type="number" 
              id="budget"
              name="budget"
              value={formData.budget}
              onChange={handleChange}
              placeholder="e.g. 1500"
              min="0"
              step="100"
            />
          </div>

          <div className="input-group">
            <label htmlFor="min_rating">Minimum Rating</label>
            <select 
              id="min_rating"
              name="min_rating"
              value={formData.min_rating}
              onChange={handleChange}
            >
              <option value="0">Any Rating</option>
              <option value="3.5">3.5 &amp; Above</option>
              <option value="4.0">4.0 &amp; Above</option>
              <option value="4.5">4.5 &amp; Above</option>
            </select>
          </div>
        </div>

        <div className="input-group full-width">
          <label htmlFor="extra">Describe your perfect meal (vibe, mood, or specific cravings)</label>
          <textarea 
            id="extra"
            name="extra"
            value={formData.extra}
            onChange={handleChange}
            placeholder="e.g. A quiet rooftop for a date, or a place with live music and great momos..."
            rows="3"
          />
        </div>

        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? (
            <>
              <div className="spinner"></div> Searching...
            </>
          ) : 'Find Restaurants'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {loading && (
        <div className="results-container">
          <h2 className="results-header">Consulting our AI Food Expert...</h2>
          <div className="cards-grid">
            {[1, 2, 3].map(i => (
              <div key={i} className="skeleton-card">
                <div className="skeleton skeleton-title"></div>
                <div className="skeleton skeleton-meta"></div>
                <br/>
                <div className="skeleton skeleton-text"></div>
                <div className="skeleton skeleton-text"></div>
                <div className="skeleton skeleton-text"></div>
              </div>
            ))}
          </div>
        </div>
      )}

      {results && !loading && (
        <div className="results-container">
          <h2 className="results-header">Your Recommendations</h2>
          {results.summary && (
            <div className="results-summary">{results.summary}</div>
          )}

          {results.recommendations.length === 0 ? (
            <div className="empty-state">
              <h3>No Perfect Matches Found</h3>
              <p>Try adjusting your filters, like broadening the location or lowering the minimum rating.</p>
            </div>
          ) : (
            <div className="cards-grid">
              {results.recommendations.map((rec, idx) => (
                <div 
                  key={rec.restaurant.id} 
                  className="result-card" 
                  style={{ animationDelay: `${idx * 0.15}s` }}
                >
                  <div className="card-header">
                    <div className="rank-badge">#{rec.rank}</div>
                    <h3 className="card-title">{rec.restaurant.name}</h3>
                    <div className="card-meta">
                      <span className="rating">★ {rec.restaurant.rating}</span>
                      <span>₹{rec.restaurant.cost_for_two} for two</span>
                    </div>
                    <div className="card-cuisines">{rec.restaurant.cuisines}</div>
                  </div>
                  <div className="card-body">
                    <p className="explanation">{rec.explanation}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
