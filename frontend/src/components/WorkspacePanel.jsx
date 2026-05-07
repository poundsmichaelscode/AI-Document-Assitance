import { useState } from 'react';
import { api } from '../services/api';
export default function WorkspacePanel({ workspaces, selectedWorkspace, onCreated, onSelect }) {
  const [name, setName] = useState('');
  async function createWorkspace(){ if(!name.trim())return; const {data}=await api.post('/workspaces',{name:name.trim()}); setName(''); onCreated(data); }
  return <section className="rounded-3xl border border-slate-800 bg-slate-900 p-5"><h2 className="text-lg font-bold">Workspaces</h2><div className="mt-4 flex gap-2"><input className="min-w-0 flex-1 rounded-xl bg-slate-950 p-3" placeholder="Workspace name" value={name} onChange={(e)=>setName(e.target.value)}/><button className="rounded-xl bg-white px-4 text-slate-950" onClick={createWorkspace}>Add</button></div><div className="mt-4 space-y-2">{workspaces.map((w)=><button key={w.id} onClick={()=>onSelect(w)} className={`w-full rounded-xl p-3 text-left ${selectedWorkspace?.id===w.id?'bg-slate-700':'bg-slate-950'}`}>{w.name}</button>)}</div></section>
}
