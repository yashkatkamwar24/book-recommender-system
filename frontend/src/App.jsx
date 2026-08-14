import "./App.css";
import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  function handleRecommend() {
    if (!query.trim()) {
      return;
    }

    const books = [
      {
        title: "The Hobbit",
        genre: "Adventure",
        description: "An exciting fantasy adventure about a hobbit."
      },
      {
        title: "Treasure Island",
        genre: "Adventure",
        description: "A thrilling pirate adventure involving treasure."
      },
      {
        title: "Pride and Prejudice",
        genre: "Romance",
        description: "A classic romantic story about love and relationships."
      }
    ];

    setRecommendations(books);
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
              Recommend
            </button>
          </div>

          <p>You searched for: {query}</p>
        </div>

        <section className="recommendations">
          <h2>Recommended Books</h2>

          <div className="book-container">
            {recommendations.map((book, index) => (
              <div className="book-card" key={index}>
                <h3>{book.title}</h3>
                <p>{book.genre}</p>
                <span>{book.description}</span>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;