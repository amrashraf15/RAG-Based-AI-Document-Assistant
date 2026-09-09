import {
  FileText,
} from "lucide-react";

import type { DocumentInfo } from "../../types/document";

import { DocumentCard } from "./DocumentCard";
import { EmptyState } from "../common/EmptyState";

interface DocumentListProps {
  documents: DocumentInfo[];
  onDelete: (document: DocumentInfo) => void;
}

export function DocumentList({
  documents,
  onDelete,
}: DocumentListProps) {
  if (documents.length === 0) {
    return (
      <EmptyState
        icon={<FileText size={25} />}
        title="No documents"
        description="Upload a PDF to start building your document knowledge base."
      />
    );
  }

  return (
    <div className="document-list">
      {documents.map((document) => (
        <DocumentCard
          key={document.document_id}
          document={document}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}