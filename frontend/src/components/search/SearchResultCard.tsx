import {
  FileText,
} from "lucide-react";

import type { SearchResult } from "../../types/search";
import { truncateText } from "../../utils/format";

interface SearchResultCardProps {
  result: SearchResult;
}

export function SearchResultCard({
  result,
}: SearchResultCardProps) {
  return (
    <article className="search-result-card">
      <div className="search-result-header">
        <div className="search-result-file">
          <FileText size={18} />

          <div>
            <strong>
              {result.filename}
            </strong>

            <span>
              Page {result.page_number}
            </span>
          </div>
        </div>

        <div className="fused-score">
          {result.fused_score.toFixed(4)}
        </div>
      </div>

      <p className="search-result-text">
        {truncateText(result.text, 450)}
      </p>

      <div className="score-grid">
        <div>
          <span>Dense</span>
          <strong>
            {result.dense_score.toFixed(4)}
          </strong>
        </div>

        <div>
          <span>Lexical</span>
          <strong>
            {result.lexical_score.toFixed(4)}
          </strong>
        </div>

        <div>
          <span>Fused</span>
          <strong>
            {result.fused_score.toFixed(4)}
          </strong>
        </div>
      </div>

      <div className="search-result-footer">
        <span>
          Chunk: {result.chunk_id}
        </span>

        <span>
          {result.embedding_model}
        </span>
      </div>
    </article>
  );
}