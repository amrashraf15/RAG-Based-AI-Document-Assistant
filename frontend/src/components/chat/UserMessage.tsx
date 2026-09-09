interface UserMessageProps {
  content: string;
}

export function UserMessage({
  content,
}: UserMessageProps) {
  return (
    <div className="message-row user-row">
      <div className="message user-message">
        {content}
      </div>
    </div>
  );
}