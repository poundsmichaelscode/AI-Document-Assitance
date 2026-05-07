import { useState } from 'react';
import { api } from '../services/api';
export default function AuthPanel({ onAuthenticated }) {
  const [mode, setMode] = useState('register');
  const [email, setEmail] = useState('owner@example.com');
  const [password, setPassword] = useState('Password123!');
  const [error, setError] = useState('');
  async function submit(e) {
    e.preventDefault(); setError('');
    try { const endpoint = mode === 'register' ? '/auth/register' : '/auth/login'; const { data } = await api.post(endpoint, { email, password }); localStorage.setItem('token', data.access_token); await onAuthenticated(); }
    catch (err) { setError(err?.response?.data?.detail || 'Authentication failed'); }
  }
  return <form onSubmit={submit} className="mx-auto max-w-md rounded-3xl border border-slate-800 bg-slate-900 p-8 shadow-2xl">
    <h1 className="text-3xl font-bold">AI Document Assistant</h1><p className="mt-2 text-slate-400">Upload documents and ask questions using RAG.</p>
    <input className="mt-6 w-full rounded-xl border border-slate-700 bg-slate-950 p-3 outline-none" value={email} onChange={(e)=>setEmail(e.target.value)} />
    <input className="mt-3 w-full rounded-xl border border-slate-700 bg-slate-950 p-3 outline-none" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
    {error && <p className="mt-3 text-rose-400">{error}</p>}
    <button className="mt-4 w-full rounded-xl bg-white p-3 font-bold text-slate-950">{mode === 'register' ? 'Create account' : 'Sign in'}</button>
    <button type="button" className="mt-3 w-full rounded-xl border border-slate-700 p-3" onClick={()=>setMode(mode==='register'?'login':'register')}>{mode==='register'?'Already have an account?':'Need an account?'}</button>
  </form>
}
