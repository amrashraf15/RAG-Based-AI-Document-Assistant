export interface Citation {
  citation_id: string;
  chunk_id: string;
  document_id: string;
  filename: string;
  page_number: number;
  text: string;
  title?: string | null;
  source: string;
}

export interface ChatRequest {
  query: string;
  top_k?: number;
  candidate_k?: number;
  dense_weight?: number;
  lexical_weight?: number;
  document_id?: string | null;
  filename?: string | null;
  conversation_id?: string | null;
  conversation_history?: ConversationMessage[];
}

export interface ChatResponse {
  query: string;
  answer: string;
  citations: Citation[];
  model: string;
  grounded: boolean;
  citation_ids: string[];
  conversation_id?: string | null;
}

export interface ConversationMessage {
  role: "user" | "assistant";
  content: string;
}

export interface Conversation {
  conversation_id: string;
  messages: ConversationMessage[];
  created_at?: string | null;
  updated_at?: string | null;
}