interface LoadingSpinnerProps {
  size?: "small" | "medium" | "large";
}

export function LoadingSpinner({
  size = "medium",
}: LoadingSpinnerProps) {
  return (
    <span
      className={`spinner spinner-${size}`}
      aria-label="Loading"
    />
  );
}