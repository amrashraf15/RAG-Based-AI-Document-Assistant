import {
  useState,
} from "react";

import { sendChatMessage } from "../api/chat";

import type {
  ChatResponse,
  ConversationMessage,
} from "../types/chat";

import { getErrorMessage } from "../utils/error";

export function useChat() {
  const [messages, setMessages] =
    useState<ChatResponse[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [pendingQuestion, setPendingQuestion] =
    useState<string | null>(null);

  const [conversationId, setConversationId] =
    useState<string | null>(null);

  const sendMessage = async (
    query: string,
  ) => {
    const trimmed = query.trim();

    if (!trimmed || loading) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setPendingQuestion(trimmed);

      const history: ConversationMessage[] =
        messages.flatMap(
          (message) => [
            {
              role: "user" as const,
              content: message.query,
            },
            {
              role: "assistant" as const,
              content: message.answer,
            },
          ],
        );

      const response =
        await sendChatMessage({
          query: trimmed,
          top_k: 5,
          candidate_k: 20,
          dense_weight: 0.5,
          lexical_weight: 0.5,
          conversation_id:
            conversationId,
          conversation_history:
            history,
        });

      setMessages((previous) => [
        ...previous,
        response,
      ]);

      if (
        response.conversation_id
      ) {
        setConversationId(
          response.conversation_id,
        );
      }
    } catch (chatError) {
      setError(
        getErrorMessage(chatError),
      );
    } finally {
      setLoading(false);
      setPendingQuestion(null);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId(null);
    setPendingQuestion(null);
    setError(null);
  };

  return {
    messages,
    loading,
    error,
    pendingQuestion,
    conversationId,
    sendMessage,
    clearChat,
  };
}