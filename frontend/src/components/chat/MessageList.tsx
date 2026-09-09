import type { ChatResponse } from "../../types/chat";

import { AssistantMessage } from "./AssistantMessage";
import { UserMessage } from "./UserMessage";

interface MessageListProps {
  messages: ChatResponse[];
  pendingQuestion?: string | null;
}

export function MessageList({
  messages,
  pendingQuestion,
}: MessageListProps) {
  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div key={`${message.query}-${index}`}>
          <UserMessage
            content={message.query}
          />

          <AssistantMessage
            content={message.answer}
            citations={message.citations}
            grounded={message.grounded}
            model={message.model}
          />
        </div>
      ))}

      {pendingQuestion && (
        <>
          <UserMessage
            content={pendingQuestion}
          />

          <div className="message-row assistant-row">
            <div className="assistant-avatar">
              <span className="typing-dots">
                <span />
                <span />
                <span />
              </span>
            </div>

            <div className="typing-message">
              Thinking...
            </div>
          </div>
        </>
      )}
    </div>
  );
}