import React, { useState } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/auth/login?email=${email}&password=${password}`, {
        method: 'POST',
      });
      const data = await res.json();
      if (data.access_token) {
        setToken(data.access_token);
        alert('Login successful!');
      }
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed');
    }
    setLoading(false);
  };

  const handleChat = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/agents/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          query,
          context: {},
          session_id: null
        })
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Chat failed:', error);
      setResponse({ error: 'Failed to get response' });
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MediSense-AI</h1>
        <p>Enterprise Clinical AI Multi-Agent Assistant</p>
      </header>

      {!token ? (
        <div className="login-container">
          <h2>Login</h2>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </div>
      ) : (
        <div className="chat-container">
          <h2>Chat with AI Assistant</h2>
          <div className="chat-input">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question or request assistance..."
              rows={4}
            />
            <button onClick={handleChat} disabled={loading || !query.trim()}>
              {loading ? 'Processing...' : 'Send'}
            </button>
          </div>

          {response && (
            <div className="response-container">
              <h3>Response:</h3>
              <div className="response-content">
                <p><strong>Agent:</strong> {response.agent_name}</p>
                <p><strong>Response:</strong> {response.response}</p>
                <p><strong>Confidence:</strong> {response.confidence}</p>
                {response.error && <p className="error">{response.error}</p>}
              </div>
            </div>
          )}

          <div className="features">
            <h3>Available Features:</h3>
            <ul>
              <li>Appointment Scheduling</li>
              <li>Clinical Consultation Chat</li>
              <li>Symptom Image Analysis</li>
              <li>Report Understanding</li>
              <li>Prescription Generation</li>
              <li>Medical Records Search</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
