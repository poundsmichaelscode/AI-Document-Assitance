import { useEffect, useState } from 'react';
import { api } from '../services/api';
export function useAuth() {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  async function loadProfile() {
    const token = localStorage.getItem('token');
    if (!token) { setAuthLoading(false); return; }
    try { const { data } = await api.get('/auth/me'); setUser(data); }
    catch { localStorage.removeItem('token'); setUser(null); }
    finally { setAuthLoading(false); }
  }
  useEffect(() => { loadProfile(); }, []);
  return { user, authLoading, loadProfile };
}
