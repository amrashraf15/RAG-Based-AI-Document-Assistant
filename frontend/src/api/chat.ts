import { apiClient } from "./client";
import type {
  ChatRequest,
  ChatResponse,
} from "../types/chat";

export async function sendChatMessage(
  request: ChatRequest,
): Promise<ChatResponse> {
  const response = await apiClient.post<ChatResponse>(
    "/chat",
    {
      query: request.query,
      top_k: request.top_k ?? 5,
      candidate_k: request.candidate_k ?? 20,
      dense_weight: request.dense_weight ?? 0.5,
      lexical_weight: request.lexical_weight ?? 0.5,
      document_id: request.document_id ?? null,
      filename: request.filename ?? null,
      conversation_id: request.conversation_id ?? null,
      conversation_history:
        request.conversation_history ?? [],
    },
  );

  return response.data;
}