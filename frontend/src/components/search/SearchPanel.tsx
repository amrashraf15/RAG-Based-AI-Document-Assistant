import {
  Search as SearchIcon,
} from "lucide-react";

import {
  useState,
} from "react";

import { searchDocuments } from "../../api/search";
import type { SearchResponse } from "../../types/search";
import { getErrorMessage } from "../../utils/error";

import { ErrorMessage } from "../common/ErrorMessage";
import { LoadingSpinner } from "../common/LoadingSpinner";
import { SearchResultCard } from "./SearchResultCard";

export function SearchPanel() {
  const [query, setQuery] =
    useState("");

  const [result, setResult] =
    useState<SearchResponse | null>(
      null,
    );

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const handleSearch = async () => {
    const trimmed = query.trim();

    if (!trimmed) {
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response =
        await searchDocuments({
          query: trimmed,
          top_k: 5,
          candidate_k: 20,
          dense_weight: 0.5,
          lexical_weight: 0.5,
        });

      setResult(response);
    } catch (searchError) {
      setError(
        getErrorMessage(searchError),
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <div className="search-bar-large">
        <SearchIcon size={20} />

        <input
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              handleSearch();
            }
          }}
          placeholder="Search your documents..."
        />

        <button
          className="primary-button"
          onClick={handleSearch}
          disabled={
            loading || !query.trim()
          }
        >
          {loading
            ? "Searching..."
            : "Search"}
        </button>
      </div>

      {error && (
        <ErrorMessage
          message={error}
          onRetry={handleSearch}
        />
      )}

      {loading && (
        <div className="center-loader">
          <LoadingSpinner size="large" />
        </div>
      )}

      {result && !loading && (
        <div className="search-results">
          <div className="results-header">
            <div>
              <h3>
                Search results
              </h3>

              <p>
                {result.count} result
                {result.count === 1
                  ? ""
                  : "s"} for "
                {result.query}"
              </p>
            </div>
          </div>

          {result.results.length === 0 ? (
            <div className="no-results">
              No relevant documents were
              found.
            </div>
          ) : (
            result.results.map((item) => (
              <SearchResultCard
                key={item.chunk_id}
                result={item}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
}