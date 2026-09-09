import { apiClient } from "./client";
import type {
  DocumentDeleteResponse,
  DocumentInfo,
  DocumentListResponse,
  DocumentUploadResponse,
} from "../types/document";

export async function uploadDocument(
  file: File,
): Promise<DocumentUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await apiClient.post<DocumentUploadResponse>(
    "/documents/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
}

export async function getDocuments(): Promise<DocumentInfo[]> {
  const response = await apiClient.get<
    DocumentListResponse | DocumentInfo[]
  >("/documents");

  if (Array.isArray(response.data)) {
    return response.data;
  }

  return response.data.documents;
}

export async function getDocument(
  documentId: string,
): Promise<DocumentInfo> {
  const response = await apiClient.get<DocumentInfo>(
    `/documents/${encodeURIComponent(documentId)}`,
  );

  return response.data;
}

export async function deleteDocument(
  documentId: string,
): Promise<DocumentDeleteResponse> {
  const response = await apiClient.delete<DocumentDeleteResponse>(
    `/documents/${encodeURIComponent(documentId)}`,
  );

  return response.data;
}