import { useEffect, useState } from 'react';
import { api, Client, Note } from './api';

const emptyClient = {
  name: '',
  company: '',
  email: '',
  status: 'Lead',
  priority: 'Medium',
  last_contact_date: ''
};

function App() {
  const [email, setEmail] = useState('demo@example.com');
  const [password, setPassword] = useState('password123');
  const [isAuthenticated, setIsAuthenticated] = useState(Boolean(localStorage.getItem('crm_token')));
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [notes, setNotes] = useState<Note[]>([]);
  const [newNote, setNewNote] = useState('');
  const [clientForm, setClientForm] = useState(emptyClient);
  const [aiResult, setAiResult] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (isAuthenticated) loadClients();
  }, [isAuthenticated]);

  async function handleAuth(mode: 'login' | 'register') {
    try {
      setError('');
      const result = mode === 'login' ? await api.login(email, password) : await api.register(email, password);
      localStorage.setItem('crm_token', result.token);
      setIsAuthenticated(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed');
    }
  }

  async function loadClients() {
    const data = await api.listClients();
    setClients(data);
    if (!selectedClient && data.length > 0) selectClient(data[0]);
  }

  async function selectClient(client: Client) {
    setSelectedClient(client);
    setAiResult('');
    const clientNotes = await api.listNotes(client.id);
    setNotes(clientNotes);
  }

  async function addClient() {
    if (!clientForm.name.trim()) return;
    await api.createClient(clientForm);
    setClientForm(emptyClient);
    await loadClients();
  }

  async function addNote() {
    if (!selectedClient || !newNote.trim()) return;
    await api.createNote(selectedClient.id, newNote);
    setNewNote('');
    await selectClient(selectedClient);
  }

  async function runAI(type: 'summary' | 'followup') {
    if (!selectedClient) return;
    setAiResult('Generating...');
    const response = type === 'summary' ? await api.summarize(selectedClient.id) : await api.followUp(selectedClient.id);
    setAiResult(response.result);
  }

  function logout() {
    localStorage.removeItem('crm_token');
    setIsAuthenticated(false);
    setClients([]);
    setSelectedClient(null);
  }

  if (!isAuthenticated) {
    return (
      <main className="auth-page">
        <section className="auth-card">
          <p className="eyebrow">Portfolio Project</p>
          <h1>AI-Powered CRM Assistant</h1>
          <p className="muted">Manage clients, notes, and AI-generated follow-ups from one full-stack dashboard.</p>
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
          <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
          {error && <p className="error">{error}</p>}
          <div className="button-row">
            <button onClick={() => handleAuth('login')}>Login</button>
            <button className="secondary" onClick={() => handleAuth('register')}>Register</button>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Full-Stack CRM</p>
          <h1>AI-Powered CRM Assistant</h1>
        </div>
        <button className="secondary" onClick={logout}>Logout</button>
      </header>

      <section className="grid">
        <aside className="panel">
          <h2>Add Client</h2>
          <input placeholder="Name" value={clientForm.name} onChange={(e) => setClientForm({ ...clientForm, name: e.target.value })} />
          <input placeholder="Company" value={clientForm.company} onChange={(e) => setClientForm({ ...clientForm, company: e.target.value })} />
          <input placeholder="Email" value={clientForm.email} onChange={(e) => setClientForm({ ...clientForm, email: e.target.value })} />
          <div className="two-col">
            <select value={clientForm.status} onChange={(e) => setClientForm({ ...clientForm, status: e.target.value })}>
              <option>Lead</option>
              <option>Contacted</option>
              <option>Negotiation</option>
              <option>Customer</option>
            </select>
            <select value={clientForm.priority} onChange={(e) => setClientForm({ ...clientForm, priority: e.target.value })}>
              <option>Low</option>
              <option>Medium</option>
              <option>High</option>
            </select>
          </div>
          <input placeholder="Last contact date" value={clientForm.last_contact_date} onChange={(e) => setClientForm({ ...clientForm, last_contact_date: e.target.value })} />
          <button onClick={addClient}>Create Client</button>
        </aside>

        <section className="panel clients-panel">
          <h2>Clients</h2>
          {clients.map((client) => (
            <article key={client.id} className={`client-card ${selectedClient?.id === client.id ? 'active' : ''}`} onClick={() => selectClient(client)}>
              <div>
                <strong>{client.name}</strong>
                <p>{client.company || 'No company'} · {client.status}</p>
              </div>
              <span className={`pill ${client.priority.toLowerCase()}`}>{client.priority}</span>
            </article>
          ))}
        </section>

        <section className="panel details-panel">
          {selectedClient ? (
            <>
              <div className="detail-header">
                <div>
                  <h2>{selectedClient.name}</h2>
                  <p className="muted">{selectedClient.email || 'No email'} · {selectedClient.company || 'No company'}</p>
                </div>
                <span className="pill">{selectedClient.status}</span>
              </div>

              <div className="button-row">
                <button onClick={() => runAI('summary')}>Summarize Client</button>
                <button className="secondary" onClick={() => runAI('followup')}>Generate Follow-up</button>
              </div>

              {aiResult && <pre className="ai-box">{aiResult}</pre>}

              <h3>Notes</h3>
              <textarea value={newNote} onChange={(e) => setNewNote(e.target.value)} placeholder="Add meeting notes, customer needs, or next steps..." />
              <button onClick={addNote}>Add Note</button>

              <div className="notes-list">
                {notes.map((note) => (
                  <article key={note.id} className="note-card">
                    <p>{note.content}</p>
                    <small>{new Date(note.created_at).toLocaleString()}</small>
                  </article>
                ))}
              </div>
            </>
          ) : (
            <p className="muted">Create or select a client to start.</p>
          )}
        </section>
      </section>
    </main>
  );
}

export default App;
