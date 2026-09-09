import { Outlet } from "react-router-dom";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

interface AppLayoutProps {
  onUpload: () => void;
  connected: boolean;
}

export function AppLayout({
  onUpload,
  connected,
}: AppLayoutProps) {
  return (
    <div className="app-shell">
      <Sidebar onUpload={onUpload} />

      <main className="main-content">
        <Header
          title="Intelligent Document AI"
          subtitle="Ask questions and search across your documents."
          connected={connected}
        />

        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}