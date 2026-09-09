import {
  AlertTriangle,
  X,
} from "lucide-react";

import type { DocumentInfo } from "../../types/document";

interface DeleteDocumentDialogProps {
  document: DocumentInfo | null;
  deleting: boolean;
  onCancel: () => void;
  onConfirm: () => void;
}

export function DeleteDocumentDialog({
  document,
  deleting,
  onCancel,
  onConfirm,
}: DeleteDocumentDialogProps) {
  if (!document) {
    return null;
  }

  return (
    <div className="modal-backdrop">
      <div className="modal small-modal">
        <div className="modal-header">
          <div className="warning-icon">
            <AlertTriangle size={22} />
          </div>

          <button
            className="icon-button"
            onClick={onCancel}
            disabled={deleting}
          >
            <X size={18} />
          </button>
        </div>

        <h3>Delete document?</h3>

        <p className="modal-description">
          Are you sure you want to delete{" "}
          <strong>{document.filename}</strong>?
          This action cannot be undone.
        </p>

        <div className="modal-actions">
          <button
            className="secondary-button"
            onClick={onCancel}
            disabled={deleting}
          >
            Cancel
          </button>

          <button
            className="danger-button"
            onClick={onConfirm}
            disabled={deleting}
          >
            {deleting
              ? "Deleting..."
              : "Delete"}
          </button>
        </div>
      </div>
    </div>
  );
}