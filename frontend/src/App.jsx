import "./App.css";
import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleRecommend() {
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/recommend?query=${encodeURIComponent(query)}`
      );

      const data = await response.json();

      console.log("Original query:", data.query);
      console.log("Corrected query:", data.corrected_query);
      console.log("Recommendations:", data.recommendations);

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setRecommendations(data.recommendations);
      
    } catch (error) {
      console.error(error);
      setError("Unable to get recommendations. Please try again.");
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>📚 Book Recommender</h1>
        <p>Find your next favorite book</p>
      </header>

      <main>
        <div className="search-section">
          <h2>What kind of book are you looking for?</h2>

          <div className="search-box">
            <input
              type="text"
              placeholder="e.g. I want adventure books"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />

            <button onClick={handleRecommend}>
              {loading ? "Finding..." : "Recommend"}
            </button>
          </div>

          {query && <p>You searched for: {query}</p>}

          {error && <p className="error">{error}</p>}
        </div>

        <section className="recommendations">
          <h2>Recommended Books</h2>

          <div className="book-container">
            {recommendations.map((book) => (
              <div className="book-card" key={book.title}>
                <div className="book-info">
                  <h3>{book.title}</h3>

                  <p className="genre">{book.genre}</p>

                  <p className="similarity">
                    ⭐ Match: {(book.similarity * 100).toFixed(0)}%
                  </p>

                  <p className="description">
                    {book.description}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {!loading &&
            recommendations.length === 0 &&
            !error &&
            query && (
              <p>No suitable books found.</p>
            )}
        </section>
      </main>
    </div>
  );
}

export default App;