import React from "react";
import { useState } from 'react';
import { api } from '../services/api';
export default function ChatPanel({ workspaceId }) {
  const [question,setQuestion]=useState('What is this document about?'); const [answer,setAnswer]=useState(''); const [sources,setSources]=useState([]);
  async function ask(){ if(!workspaceId)return; try{ const {data}=await api.post('/chat/ask',{workspace_id:workspaceId,question,top_k:5}); setAnswer(data.answer); setSources(data.sources||[]); } catch(err){ setAnswer(err?.response?.data?.detail || 'Failed to ask question'); } }
  return <section className="rounded-3xl border border-slate-800 bg-slate-900 p-5"><h2 className="text-lg font-bold">Ask Your Documents</h2><textarea className="mt-4 h-28 w-full rounded-xl bg-slate-950 p-3" value={question} onChange={(e)=>setQuestion(e.target.value)}/><button className="mt-4 rounded-xl bg-white px-4 py-2 text-slate-950" onClick={ask}>Ask</button><div className="mt-4 whitespace-pre-wrap rounded-xl bg-slate-950 p-4">{answer||'Answer will show here.'}</div><div className="mt-4 space-y-2">{sources.map((s,i)=><div key={i} className="rounded-xl border border-slate-800 p-3 text-sm">{s.file_name}: {s.snippet}</div>)}</div></section>
}
