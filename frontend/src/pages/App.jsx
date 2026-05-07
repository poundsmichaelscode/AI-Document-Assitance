import { useEffect, useState } from 'react';
import AuthPanel from '../components/AuthPanel';
import WorkspacePanel from '../components/WorkspacePanel';
import FileUpload from '../components/FileUpload';
import DocumentList from '../components/DocumentList';
import ChatPanel from '../components/ChatPanel';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
export default function App() {
  const { user, authLoading, loadProfile } = useAuth();
  const [workspaces,setWorkspaces]=useState([]); const [selectedWorkspace,setSelectedWorkspace]=useState(null); const [documents,setDocuments]=useState([]);
  async function loadWorkspaces(){ const {data}=await api.get('/workspaces'); setWorkspaces(data); if(!selectedWorkspace&&data.length)setSelectedWorkspace(data[0]);}
  async function loadDocuments(workspaceId=selectedWorkspace?.id){ if(!workspaceId)return; const {data}=await api.get('/documents',{params:{workspace_id:workspaceId}}); setDocuments(data);}
  useEffect(()=>{ if(user) loadWorkspaces(); },[user]);
  useEffect(()=>{ if(selectedWorkspace?.id) loadDocuments(selectedWorkspace.id); },[selectedWorkspace]);
  if(authLoading) return <main className="grid min-h-screen place-items-center bg-slate-950 text-white">Loading...</main>;
  if(!user) return <main className="min-h-screen bg-slate-950 px-6 py-16 text-white"><AuthPanel onAuthenticated={loadProfile}/></main>;
  return <main className="min-h-screen bg-slate-950 px-6 py-8 text-white"><div className="mx-auto max-w-7xl"><header className="mb-8 flex justify-between"><h1 className="text-2xl font-bold">AI Document Assistant</h1><button onClick={()=>{localStorage.removeItem('token');location.reload();}}>Sign out</button></header><div className="grid gap-6 lg:grid-cols-12"><div className="lg:col-span-3"><WorkspacePanel workspaces={workspaces} selectedWorkspace={selectedWorkspace} onSelect={setSelectedWorkspace} onCreated={(w)=>{setWorkspaces([w,...workspaces]);setSelectedWorkspace(w);}}/></div><div className="space-y-6 lg:col-span-4"><FileUpload workspaceId={selectedWorkspace?.id} onUploaded={()=>loadDocuments()}/><DocumentList documents={documents} onRefresh={()=>loadDocuments()}/></div><div className="lg:col-span-5"><ChatPanel workspaceId={selectedWorkspace?.id}/></div></div></div></main>
}
