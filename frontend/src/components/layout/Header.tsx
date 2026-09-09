import {
  Activity,
  Circle,
} from "lucide-react";

interface HeaderProps {
  title: string;
  subtitle?: string;
  connected: boolean;
}

export function Header({
  title,
  subtitle,
  connected,
}: HeaderProps) {
  return (
    <header className="header">
      <div>
        <h2>{title}</h2>

        {subtitle && (
          <p>{subtitle}</p>
        )}
      </div>

      <div
        className={
          connected
            ? "connection-status connected"
            : "connection-status disconnected"
        }
      >
        <Circle size={9} fill="currentColor" />

        <span>
          {connected
            ? "API Connected"
            : "API Offline"}
        </span>

        <Activity size={16} />
      </div>
    </header>
  );
}