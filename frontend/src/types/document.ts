export interface DocumentInfo {
  document_id: string;
  filename: string;
  source?: string | null;
  title?: string | null;
  page_count?: number;
  extracted_character_count?: number;
  cleaned_character_count?: number;
  size_bytes?: number;
  status?: string;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface DocumentUploadResponse {
  status: string;
  document_id: string;
  filename: string;
  size_bytes: number;
  path?: string;
}

export interface DocumentListResponse {
  documents: DocumentInfo[];
  count: number;
}

export interface DocumentDeleteResponse {
  status: string;
  document_id: string;
  message?: string;
}