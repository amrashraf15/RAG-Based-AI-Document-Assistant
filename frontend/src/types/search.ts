export interface SearchRequest {
  query: string;
  top_k?: number;
  candidate_k?: number;
  dense_weight?: number;
  lexical_weight?: number;
  document_id?: string | null;
  filename?: string | null;
}

export interface SearchResult {
  chunk_id: string;
  document_id: string;
  filename: string;
  page_number: number;
  chunk_index: number;
  text: string;
  dense_score: number;
  lexical_score: number;
  fused_score: number;
  title?: string | null;
  source: string;
  token_count: number;
  character_count: number;
  embedding_model: string;
  embedding_dimension: number;
  normalized: boolean;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  count: number;
}