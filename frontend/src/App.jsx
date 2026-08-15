import "./App.css";
import { useState } from "react";

import hobbitCover from "./assets/the_hobbit_cover.png";
import treasureIslandCover from "./assets/treasure_island_cover.png";
import pridePrejudiceCover from "./assets/pride_and_prejudice_cover.png";

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
        author: "J.R.R. Tolkien",
        genre: "Adventure",
        rating: 4.8,
        popularity: "Very Popular",
        description:
          "An exciting fantasy adventure about a hobbit who goes on an unexpected journey.",
        cover: hobbitCover,
      },
      {
        title: "Treasure Island",
        author: "Robert Louis Stevenson",
        genre: "Adventure",
        rating: 4.6,
        popularity: "Popular",
        description:
          "A thrilling pirate adventure involving treasure, ships, and a mysterious island.",
        cover: treasureIslandCover,
      },
      {
        title: "Pride and Prejudice",
        author: "Jane Austen",
        genre: "Romance",
        rating: 4.7,
        popularity: "Classic",
        description:
          "A classic romantic story about love, relationships, and social expectations.",
        cover: pridePrejudiceCover,
      },
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

            <button onClick={handleRecommend}>Recommend</button>
          </div>

          {query && <p>You searched for: {query}</p>}
        </div>

        <section className="recommendations">
          <h2>Recommended Books</h2>

          <div className="book-container">
            {recommendations.map((book) => (
              <div className="book-card" key={book.title}>
                <img
                  src={book.cover}
                  alt={`${book.title} book cover`}
                  className="book-cover"
                />

                <div className="book-info">
                  <h3>{book.title}</h3>

                  <p className="author">by {book.author}</p>

                  <p className="genre">{book.genre}</p>

                  <div className="book-meta">
                    <span>⭐ {book.rating}</span>
                    <span>🔥 {book.popularity}</span>
                  </div>

                  <p className="description">{book.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;