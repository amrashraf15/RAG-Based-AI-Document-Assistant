import { apiClient } from "./client";
import type { Conversation } from "../types/chat";

export async function getConversation(
  conversationId: string,
): Promise<Conversation> {
  const response = await apiClient.get<Conversation>(
    `/conversations/${encodeURIComponent(conversationId)}`,
  );

  return response.data;
}