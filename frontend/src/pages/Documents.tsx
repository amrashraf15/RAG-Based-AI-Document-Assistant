import {
  Plus,
  RefreshCw,
} from "lucide-react";

import {
  useState,
} from "react";

import type { DocumentInfo } from "../types/document";

import { DocumentList } from "../components/documents/DocumentList";
import { DeleteDocumentDialog } from "../components/documents/DeleteDocumentDialog";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorMessage } from "../components/common/ErrorMessage";
import { useDocuments } from "../hooks/useDocuments";

interface DocumentsProps {
  onUpload: () => void;
}

export function Documents({
  onUpload,
}: DocumentsProps) {
  const {
    documents,
    loading,
    error,
    refresh,
    removeDocument,
  } = useDocuments();

  const [selectedDocument, setSelectedDocument] =
    useState<DocumentInfo | null>(null);

  const [deleting, setDeleting] =
    useState(false);

  const handleDelete = async () => {
    if (!selectedDocument) {
      return;
    }

    try {
      setDeleting(true);

      await removeDocument(
        selectedDocument.document_id,
      );

      setSelectedDocument(null);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="documents-page">
      <div className="page-toolbar">
        <div>
          <h2>Documents</h2>

          <p>
            {documents.length} document
            {documents.length === 1
              ? ""
              : "s"} in your knowledge base.
          </p>
        </div>

        <div className="toolbar-actions">
          <button
            className="secondary-button"
            onClick={() => void refresh()}
            disabled={loading}
          >
            <RefreshCw size={16} />
            Refresh
          </button>

          <button
            className="primary-button"
            onClick={onUpload}
          >
            <Plus size={17} />
            Upload PDF
          </button>
        </div>
      </div>

      {error && (
        <ErrorMessage
          message={error}
          onRetry={() => void refresh()}
        />
      )}

      {loading ? (
        <div className="center-loader">
          <LoadingSpinner size="large" />
        </div>
      ) : (
        <DocumentList
          documents={documents}
          onDelete={setSelectedDocument}
        />
      )}

      <DeleteDocumentDialog
        document={selectedDocument}
        deleting={deleting}
        onCancel={() =>
          setSelectedDocument(null)
        }
        onConfirm={() =>
          void handleDelete()
        }
      />
    </div>
  );
}