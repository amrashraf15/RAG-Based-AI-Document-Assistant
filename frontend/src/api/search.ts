import { apiClient } from "./client";
import type {
  SearchRequest,
  SearchResponse,
} from "../types/search";

export async function searchDocuments(
  request: SearchRequest,
): Promise<SearchResponse> {
  const response = await apiClient.post<SearchResponse>(
    "/search",
    {
      query: request.query,
      top_k: request.top_k ?? 5,
      candidate_k: request.candidate_k ?? 20,
      dense_weight: request.dense_weight ?? 0.5,
      lexical_weight: request.lexical_weight ?? 0.5,
      document_id: request.document_id ?? null,
      filename: request.filename ?? null,
    },
  );

  return response.data;
}