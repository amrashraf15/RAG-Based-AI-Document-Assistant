import {
  FileText,
  Trash2,
} from "lucide-react";

import type { DocumentInfo } from "../../types/document";
import {
  formatDate,
  formatFileSize,
} from "../../utils/format";
import { StatusBadge } from "../common/StatusBadge";

interface DocumentCardProps {
  document: DocumentInfo;
  onDelete: (document: DocumentInfo) => void;
}

export function DocumentCard({
  document,
  onDelete,
}: DocumentCardProps) {
  return (
    <article className="document-card">
      <div className="document-card-icon">
        <FileText size={22} />
      </div>

      <div className="document-card-content">
        <h3 title={document.filename}>
          {document.filename}
        </h3>

        <div className="document-meta">
          {document.page_count !== undefined && (
            <span>
              {document.page_count}{" "}
              {document.page_count === 1
                ? "page"
                : "pages"}
            </span>
          )}

          {document.size_bytes !== undefined && (
            <span>
              {formatFileSize(
                document.size_bytes,
              )}
            </span>
          )}

          {document.created_at && (
            <span>
              {formatDate(
                document.created_at,
              )}
            </span>
          )}
        </div>

        <StatusBadge
          status={
            document.status ?? "Ready"
          }
        />
      </div>

      <button
        className="danger-icon-button"
        onClick={() => onDelete(document)}
        aria-label={`Delete ${document.filename}`}
      >
        <Trash2 size={17} />
      </button>
    </article>
  );
}