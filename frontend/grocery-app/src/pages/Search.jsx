import React, { useState, useContext, useEffect} from 'react';
import SearchResults from '../components/SearchResults';
import { ListContext } from '../context/ListContext';
import '../styles/App.css'

const Search = () => {
  const [query, setQuery] = useState("");
  // Pull feedback + clearer from context
  const { feedback, setFeedback } = useContext(ListContext);

  return (
    <div className="search-area">
      {/* Feedback banner  */}
      {feedback && (
        <div className="feedback">
          <span>{feedback}</span>
          <button
            className="feedback-close"
            onClick={() => setFeedback("")}
            aria-label="Dismiss message"
          >
            ×
          </button>
        </div>
      )}

      <input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-bar"
      />

      <SearchResults query={query} />
    </div>
  );
};

export default Search;
