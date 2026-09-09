import { Search as SearchIcon } from "lucide-react";

import { SearchPanel } from "../components/search/SearchPanel";

export function Search() {
  return (
    <div className="search-page-wrapper">
      <div className="page-toolbar">
        <div>
          <h2>Document Search</h2>

          <p>
            Inspect dense, lexical, and hybrid
            retrieval results.
          </p>
        </div>

        <div className="retrieval-badge">
          <SearchIcon size={15} />
          Hybrid Retrieval
        </div>
      </div>

      <SearchPanel />
    </div>
  );
}