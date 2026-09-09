import {
  FileText,
  ExternalLink,
} from "lucide-react";

import type { Citation } from "../../types/chat";
import { truncateText } from "../../utils/format";

interface CitationCardProps {
  citation: Citation;
}

export function CitationCard({
  citation,
}: CitationCardProps) {
  return (
    <div className="citation-card">
      <div className="citation-icon">
        <FileText size={16} />
      </div>

      <div className="citation-content">
        <div className="citation-title">
          <strong>
            [{citation.citation_id}]
          </strong>

          <span>
            {citation.filename}
          </span>
        </div>

        <span className="citation-page">
          Page {citation.page_number}
        </span>

        <p>
          {truncateText(
            citation.text,
            260,
          )}
        </p>
      </div>

      <ExternalLink size={15} />
    </div>
  );
}