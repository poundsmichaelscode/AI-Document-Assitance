import React from "react";
import { useEffect, useState } from "react";
import AuthPanel from "../components/AuthPanel";
import WorkspacePanel from "../components/WorkspacePanel";
import FileUpload from "../components/FileUpload";
import DocumentList from "../components/DocumentList";
import ChatPanel from "../components/ChatPanel";
import { useAuth } from "../hooks/useAuth";
import { api } from "../services/api";



export default function App() {
  const { user, authLoading, loadProfile } = useAuth();

  const [workspaces, setWorkspaces] = useState([]);
  const [selectedWorkspace, setSelectedWorkspace] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState("");

  async function loadWorkspaces() {
    try {
      const { data } = await api.get("/workspaces");
      setWorkspaces(data);

      if (!selectedWorkspace && data.length > 0) {
        setSelectedWorkspace(data[0]);
      }
    } catch (err) {
      console.error(err);
      setError("Could not load workspaces. Check if backend is running.");
    }
  }

  async function loadDocuments(workspaceId = selectedWorkspace?.id) {
    if (!workspaceId) return;

    try {
      const { data } = await api.get("/documents", {
        params: { workspace_id: workspaceId }
      });
      setDocuments(data);
    } catch (err) {
      console.error(err);
      setError("Could not load documents.");
    }
  }

  useEffect(() => {
    if (user) loadWorkspaces();
  }, [user]);

  useEffect(() => {
    if (selectedWorkspace?.id) loadDocuments(selectedWorkspace.id);
  }, [selectedWorkspace]);

  if (authLoading) {
    return (
      <main className="grid min-h-screen place-items-center bg-slate-950 text-white">
        <div className="rounded-2xl bg-slate-900 p-6">
          Loading app...
        </div>
      </main>
    );
  }

  if (!user) {
    return (
      <main className="min-h-screen bg-slate-950 px-6 py-16 text-white">
        <AuthPanel onAuthenticated={loadProfile} />
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-8 text-white">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <p className="text-sm text-slate-400">AI Document Assistant</p>
            <h1 className="text-2xl font-bold">{user.email}</h1>
          </div>

          <button
            className="rounded-xl border border-slate-700 px-4 py-2"
            onClick={() => {
              localStorage.removeItem("token");
              window.location.reload();
            }}
          >
            Sign out
          </button>
        </header>

        {error && (
          <div className="mb-6 rounded-xl border border-red-500 bg-red-950 p-4 text-red-200">
            {error}
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-12">
          <div className="lg:col-span-3">
            <WorkspacePanel
              workspaces={workspaces}
              selectedWorkspace={selectedWorkspace}
              onSelect={setSelectedWorkspace}
              onCreated={(workspace) => {
                setWorkspaces((prev) => [workspace, ...prev]);
                setSelectedWorkspace(workspace);
              }}
            />
          </div>

          <div className="space-y-6 lg:col-span-4">
            <FileUpload
              workspaceId={selectedWorkspace?.id}
              onUploaded={() => loadDocuments(selectedWorkspace?.id)}
            />

            <DocumentList
              documents={documents}
              onRefresh={() => loadDocuments(selectedWorkspace?.id)}
            />
          </div>

          <div className="lg:col-span-5">
            <ChatPanel workspaceId={selectedWorkspace?.id} />
          </div>
        </div>
      </div>
    </main>
  );
}