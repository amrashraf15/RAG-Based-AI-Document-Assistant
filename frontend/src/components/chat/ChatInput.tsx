import {
  Send,
} from "lucide-react";

import {
  useState,
} from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({
  onSend,
  disabled = false,
}: ChatInputProps) {
  const [value, setValue] =
    useState("");

  const submit = () => {
    const message = value.trim();

    if (!message || disabled) {
      return;
    }

    onSend(message);
    setValue("");
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>,
  ) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      submit();
    }
  };

  return (
    <div className="chat-input-container">
      <textarea
        value={value}
        onChange={(event) =>
          setValue(event.target.value)
        }
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about your documents..."
        disabled={disabled}
        rows={1}
      />

      <button
        className="send-button"
        onClick={submit}
        disabled={
          disabled || !value.trim()
        }
        aria-label="Send message"
      >
        <Send size={18} />
      </button>

      <div className="input-hint">
        Press Enter to send · Shift + Enter
        for a new line
      </div>
    </div>
  );
}