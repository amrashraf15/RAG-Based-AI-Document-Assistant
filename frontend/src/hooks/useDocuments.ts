
import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  deleteDocument,
  getDocuments,
} from "../api/documents";

import type { DocumentInfo } from "../types/document";
import { getErrorMessage } from "../utils/error";

export function useDocuments() {
  const [documents, setDocuments] =
    useState<DocumentInfo[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const loadDocuments =
    useCallback(async () => {
      try {
        setLoading(true);
        setError(null);

        const data =
          await getDocuments();

        setDocuments(data);
      } catch (loadError) {
        setError(
          getErrorMessage(loadError),
        );
      } finally {
        setLoading(false);
      }
    }, []);

  const removeDocument =
    useCallback(
      async (documentId: string) => {
        await deleteDocument(documentId);

        await loadDocuments();
      },
      [loadDocuments],
    );

  useEffect(() => {
    let cancelled = false;

    const fetchDocuments = async () => {
      try {
        const data =
          await getDocuments();

        if (!cancelled) {
          setDocuments(data);
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            getErrorMessage(loadError),
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void fetchDocuments();

    return () => {
      cancelled = true;
    };
  }, []);

  return {
    documents,
    loading,
    error,
    refresh: loadDocuments,
    removeDocument,
  };
}

