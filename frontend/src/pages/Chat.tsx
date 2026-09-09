import {
  Trash2,
} from "lucide-react";

import { ChatWindow } from "../components/chat/ChatWindow";
import { ErrorMessage } from "../components/common/ErrorMessage";
import { useChat } from "../hooks/useChat";

export function Chat() {
  const {
    messages,
    loading,
    error,
    pendingQuestion,
    sendMessage,
    clearChat,
  } = useChat();

  return (
    <div className="chat-page">
      <div className="page-toolbar">
        <div>
          <h2>AI Assistant</h2>
          <p>
            Ask questions about your indexed
            documents.
          </p>
        </div>

        {messages.length > 0 && (
          <button
            className="secondary-button"
            onClick={clearChat}
          >
            <Trash2 size={16} />
            Clear chat
          </button>
        )}
      </div>

      {error && (
        <ErrorMessage message={error} />
      )}

      <ChatWindow
        messages={messages}
        loading={loading}
        pendingQuestion={pendingQuestion}
        onSend={sendMessage}
      />
    </div>
  );
}