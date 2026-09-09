import {
  FileText,
  MessageSquare,
  Search,
  Upload,
} from "lucide-react";

import {
  Link,
} from "react-router-dom";

import type { DocumentInfo } from "../types/document";

interface DashboardProps {
  documents: DocumentInfo[];
  onUpload: () => void;
}

export function Dashboard({
  documents,
  onUpload,
}: DashboardProps) {
  return (
    <div className="dashboard-page">
      <section className="hero-card">
        <div>
          <span className="eyebrow">
            AI DOCUMENT ASSISTANT
          </span>

          <h1>
            Ask questions.
            <br />
            Get grounded answers.
          </h1>

          <p>
            Search and reason over your
            documents using semantic retrieval,
            hybrid search, and citation-backed
            generation.
          </p>

          <div className="hero-actions">
            <button
              className="primary-button"
              onClick={onUpload}
            >
              <Upload size={17} />
              Upload PDF
            </button>

            <Link
              to="/chat"
              className="secondary-button"
            >
              <MessageSquare size={17} />
              Start chatting
            </Link>
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-orb">
            <FileText size={52} />
          </div>
        </div>
      </section>

      <section className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <FileText size={19} />
          </div>

          <span>Documents</span>
          <strong>{documents.length}</strong>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Search size={19} />
          </div>

          <span>Retrieval</span>
          <strong>Hybrid</strong>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <MessageSquare size={19} />
          </div>

          <span>Generation</span>
          <strong>Grounded</strong>
        </div>
      </section>

      <section className="quick-actions">
        <h2>Quick actions</h2>

        <div className="quick-action-grid">
          <Link to="/chat">
            <MessageSquare size={22} />
            <strong>Ask a question</strong>
            <span>
              Ask the AI about your documents.
            </span>
          </Link>

          <Link to="/documents">
            <FileText size={22} />
            <strong>Manage documents</strong>
            <span>
              View and manage your knowledge base.
            </span>
          </Link>

          <Link to="/search">
            <Search size={22} />
            <strong>Semantic search</strong>
            <span>
              Inspect retrieval results directly.
            </span>
          </Link>
        </div>
      </section>
    </div>
  );
}