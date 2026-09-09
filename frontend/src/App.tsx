import {
  useState,
} from "react";

import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import { AppLayout } from "./components/layout/AppLayout";
import { UploadDocument } from "./components/documents/UploadDocument";

import { Dashboard } from "./pages/Dashboard";
import { Chat } from "./pages/Chat";
import { Documents } from "./pages/Documents";
import { Search } from "./pages/Search";

import { useDocuments } from "./hooks/useDocuments";
import { useHealth } from "./hooks/useHealth";

export default function App() {
  const [uploadOpen, setUploadOpen] =
    useState(false);

  const {
    documents,
    refresh,
  } = useDocuments();

  const {
    connected,
  } = useHealth();

  return (
    <BrowserRouter>
      <Routes>
        <Route
          element={
            <AppLayout
              onUpload={() =>
                setUploadOpen(true)
              }
              connected={connected}
            />
          }
        >
          <Route
            path="/"
            element={
              <Dashboard
                documents={documents}
                onUpload={() =>
                  setUploadOpen(true)
                }
              />
            }
          />

          <Route
            path="/chat"
            element={<Chat />}
          />

          <Route
            path="/documents"
            element={
              <Documents
                onUpload={() =>
                  setUploadOpen(true)
                }
              />
            }
          />

          <Route
            path="/search"
            element={<Search />}
          />
        </Route>
      </Routes>

      <UploadDocument
        open={uploadOpen}
        onClose={() =>
          setUploadOpen(false)
        }
        onUploaded={() =>
          void refresh()
        }
      />
    </BrowserRouter>
  );
}