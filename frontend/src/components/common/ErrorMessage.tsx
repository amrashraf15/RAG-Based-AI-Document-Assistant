import { AlertCircle } from "lucide-react";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorMessage({
  message,
  onRetry,
}: ErrorMessageProps) {
  return (
    <div className="error-message">
      <AlertCircle size={18} />

      <div>
        <strong>Something went wrong</strong>
        <p>{message}</p>

        {onRetry && (
          <button
            className="text-button"
            onClick={onRetry}
          >
            Try again
          </button>
        )}
      </div>
    </div>
  );
}