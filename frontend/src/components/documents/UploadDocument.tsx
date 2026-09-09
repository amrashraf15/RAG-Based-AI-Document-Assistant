import {
  FileUp,
  X,
} from "lucide-react";
import {
  useRef,
  useState,
} from "react";

import { uploadDocument } from "../../api/documents";
import { getErrorMessage } from "../../utils/error";

interface UploadDocumentProps {
  open: boolean;
  onClose: () => void;
  onUploaded: () => void;
}

export function UploadDocument({
  open,
  onClose,
  onUploaded,
}: UploadDocumentProps) {
  const inputRef =
    useRef<HTMLInputElement>(null);

  const [file, setFile] =
    useState<File | null>(null);

  const [uploading, setUploading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const selected =
      event.target.files?.[0] ?? null;

    setError(null);

    if (!selected) {
      setFile(null);
      return;
    }

    if (
      selected.type !== "application/pdf" &&
      !selected.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {
      setError("Only PDF files are supported.");
      setFile(null);
      return;
    }

    setFile(selected);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }

    try {
      setUploading(true);
      setError(null);

      await uploadDocument(file);

      setFile(null);

      if (inputRef.current) {
        inputRef.current.value = "";
      }

      onUploaded();
      onClose();
    } catch (uploadError) {
      setError(
        getErrorMessage(uploadError),
      );
    } finally {
      setUploading(false);
    }
  };

  if (!open) {
    return null;
  }

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <div className="modal-header">
          <div>
            <h3>Upload document</h3>
            <p>
              Add a PDF to your document knowledge base.
            </p>
          </div>

          <button
            className="icon-button"
            onClick={onClose}
            disabled={uploading}
            aria-label="Close"
          >
            <X size={19} />
          </button>
        </div>

        <div className="upload-area">
          <FileUp size={38} />

          <strong>
            {file
              ? file.name
              : "Choose a PDF document"}
          </strong>

          <span>
            {file
              ? `${(
                  file.size /
                  (1024 * 1024)
                ).toFixed(2)} MB`
              : "PDF files only"}
          </span>

          <button
            className="secondary-button"
            onClick={() =>
              inputRef.current?.click()
            }
            disabled={uploading}
          >
            Choose file
          </button>

          <input
            ref={inputRef}
            type="file"
            accept=".pdf,application/pdf"
            hidden
            onChange={handleFileChange}
          />
        </div>

        {error && (
          <div className="inline-error">
            {error}
          </div>
        )}

        <div className="modal-actions">
          <button
            className="secondary-button"
            onClick={onClose}
            disabled={uploading}
          >
            Cancel
          </button>

          <button
            className="primary-button"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading
              ? "Uploading..."
              : "Upload PDF"}
          </button>
        </div>
      </div>
    </div>
  );
}