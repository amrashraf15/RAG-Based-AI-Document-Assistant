interface StatusBadgeProps {
  status: string;
}

export function StatusBadge({
  status,
}: StatusBadgeProps) {
  const normalized = status.toLowerCase();

  let className = "status-badge";

  if (
    normalized === "ready" ||
    normalized === "indexed" ||
    normalized === "success"
  ) {
    className += " status-success";
  } else if (
    normalized === "processing" ||
    normalized === "uploading"
  ) {
    className += " status-processing";
  } else if (
    normalized === "error" ||
    normalized === "failed"
  ) {
    className += " status-error";
  } else {
    className += " status-neutral";
  }

  return (
    <span className={className}>
      <span className="status-dot" />
      {status}
    </span>
  );
}