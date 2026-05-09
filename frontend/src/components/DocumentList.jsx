import React from "react";
export default function DocumentList({ documents, onRefresh }) {
  return <section className="rounded-3xl border border-slate-800 bg-slate-900 p-5"><div className="flex justify-between"><h2 className="text-lg font-bold">Documents</h2><button onClick={onRefresh} className="rounded-xl border border-slate-700 px-3">Refresh</button></div><div className="mt-4 space-y-2">{documents.map((doc)=><div key={doc.id} className="rounded-xl bg-slate-950 p-3"><div className="flex justify-between gap-3"><span>{doc.file_name}</span><span className="text-sm text-slate-400">{doc.status}</span></div>{doc.error_message&&<p className="mt-2 text-sm text-rose-400">{doc.error_message}</p>}</div>)}</div></section>
}
