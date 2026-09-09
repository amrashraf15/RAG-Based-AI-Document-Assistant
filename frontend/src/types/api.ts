export interface HealthResponse {
  status: string;
  application: string;
  version: string;
  rag_initialized: boolean;
  llm_provider: string;
  llm_model: string;
  embedding_model: string;
  qdrant_collection: string;
}

export interface ApiError {
  detail?: string;
  message?: string;
}