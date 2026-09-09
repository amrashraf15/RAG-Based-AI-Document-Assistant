import {
  MessageSquare,
} from "lucide-react";

import type { ChatResponse } from "../../types/chat";

import { EmptyState } from "../common/EmptyState";
import { ChatInput } from "./ChatInput";
import { MessageList } from "./MessageList";


interface ChatWindowProps {
  messages: ChatResponse[];
  loading: boolean;
  pendingQuestion?: string | null;
  onSend: (message: string) => void;
}

export function ChatWindow({
  messages,
  loading,
  pendingQuestion,
  onSend,
}: ChatWindowProps) {
  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.length === 0 &&
        !pendingQuestion ? (
          <div className="chat-empty">
            <EmptyState
              icon={
                <MessageSquare size={27} />
              }
              title="Ask your documents"
              description="Upload documents and ask questions about their content."
            />

            <div className="suggestion-grid">
              <button
                onClick={() =>
                  onSend(
                    "What information is available in these documents?",
                  )
                }
              >
                What information is available?
              </button>

              <button
                onClick={() =>
                  onSend(
                    "Summarize the main topics in the documents.",
                  )
                }
              >
                Summarize the documents
              </button>
            </div>
          </div>
        ) : (
          <MessageList
            messages={messages}
            pendingQuestion={
              pendingQuestion
            }
          />
        )}
      </div>

      <ChatInput
        onSend={onSend}
        disabled={loading}
      />
    </div>
  );
}