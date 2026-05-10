const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export type Client = {
  id: number;
  name: string;
  company: string;
  email: string;
  status: string;
  priority: string;
  last_contact_date: string;
};

export type Note = {
  id: number;
  content: string;
  created_at: string;
};

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('crm_token');
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {})
    }
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}

export const api = {
  register: (email: string, password: string) =>
    request<{ token: string; email: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    }),
  login: (email: string, password: string) =>
    request<{ token: string; email: string }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    }),
  listClients: () => request<Client[]>('/clients'),
  createClient: (client: Omit<Client, 'id'>) =>
    request<Client>('/clients', { method: 'POST', body: JSON.stringify(client) }),
  deleteClient: (id: number) => request<{ deleted: boolean }>(`/clients/${id}`, { method: 'DELETE' }),
  listNotes: (clientId: number) => request<Note[]>(`/clients/${clientId}/notes`),
  createNote: (clientId: number, content: string) =>
    request<Note>(`/clients/${clientId}/notes`, { method: 'POST', body: JSON.stringify({ content }) }),
  summarize: (clientId: number) =>
    request<{ result: string }>(`/ai/client-summary/${clientId}`, { method: 'POST' }),
  followUp: (clientId: number) =>
    request<{ result: string }>(`/ai/follow-up/${clientId}`, { method: 'POST' })
};
