import {
  FileText,
  LayoutDashboard,
  MessageSquare,
  Search,
  Upload,
} from "lucide-react";
import { NavLink } from "react-router-dom";

interface SidebarProps {
  onUpload: () => void;
}

export function Sidebar({
  onUpload,
}: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">
          <FileText size={21} />
        </div>

        <div>
          <h1>Intelligent</h1>
          <span>Document AI</span>
        </div>
      </div>

      <button
        className="upload-button"
        onClick={onUpload}
      >
        <Upload size={18} />
        Upload PDF
      </button>

      <nav className="sidebar-nav">
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <LayoutDashboard size={18} />
          Dashboard
        </NavLink>

        <NavLink
          to="/chat"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <MessageSquare size={18} />
          Chat
        </NavLink>

        <NavLink
          to="/documents"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <FileText size={18} />
          Documents
        </NavLink>

        <NavLink
          to="/search"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          <Search size={18} />
          Search
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <span>RAG Document Assistant</span>
        <span>v0.1.0</span>
      </div>
    </aside>
  );
}