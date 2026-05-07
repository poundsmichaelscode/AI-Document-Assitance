import { useState } from 'react';
import { api } from '../services/api';
export default function FileUpload({ workspaceId, onUploaded }) {
  const [file,setFile]=useState(null); const [message,setMessage]=useState('');
  async function upload(){ if(!workspaceId||!file)return; const form=new FormData(); form.append('workspace_id',workspaceId); form.append('file',file); try{ const {data}=await api.post('/documents/upload',form,{headers:{'Content-Type':'multipart/form-data'}}); setMessage(`Queued: ${data.file_name}`); onUploaded(); } catch(err){ setMessage(err?.response?.data?.detail || 'Upload failed'); } }
  return <section className="rounded-3xl border border-slate-800 bg-slate-900 p-5"><h2 className="text-lg font-bold">Upload Document</h2><input className="mt-4 w-full rounded-xl bg-slate-950 p-3" type="file" accept=".pdf,.docx,.txt" onChange={(e)=>setFile(e.target.files?.[0])}/><button className="mt-4 rounded-xl bg-white px-4 py-2 text-slate-950" onClick={upload}>Upload</button>{message&&<p className="mt-3 text-slate-300">{message}</p>}</section>
}
