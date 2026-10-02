import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, ChevronDown, ChevronRight, Database, Table2 } from 'lucide-react';
import { sendChatMessage } from '../../api/client';
import './AgentUI.css';

function DataTable({ tableData }) {
  if (!tableData || !tableData.columns || !tableData.rows.length) return null;

  return (
    <div className="data-table-wrapper">
      <div className="data-table-header">
        <Table2 size={14} />
        <span>
          {tableData.truncated
            ? `Showing ${tableData.rows.length} of ${tableData.total_rows} rows`
            : `${tableData.total_rows} row${tableData.total_rows !== 1 ? 's' : ''}`}
        </span>
      </div>
      <div className="data-table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              {tableData.columns.map((col, i) => (
                <th key={i}>{col.replace(/_/g, ' ')}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.rows.map((row, ri) => (
              <tr key={ri}>
                {tableData.columns.map((col, ci) => (
                  <td key={ci}>{row[col] ?? '—'}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ToolCallCard({ tool }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="tool-call-card">
      <button className="tool-call-header" onClick={() => setExpanded(!expanded)}>
        <span className="tool-call-icon"><Database size={14} /></span>
        <span className="tool-call-name">{tool.name || 'tool'}</span>
        <span className={`tool-call-status ${tool.status}`}>{tool.status}</span>
        {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
      </button>
      {expanded && (
        <div className="tool-call-details">
          {tool.input && (
            <div className="tool-detail-section">
              <span className="tool-detail-label">SQL Query</span>
              <pre className="tool-detail-content">{tool.input}</pre>
            </div>
          )}
          {tool.output && (
            <div className="tool-detail-section">
              <span className="tool-detail-label">Result</span>
              <pre className="tool-detail-content">{tool.output}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function SuggestedQueries({ queries, onSelect }) {
  if (!queries || !queries.length) return null;

  return (
    <div className="suggested-queries">
      {queries.map((q, i) => (
        <button key={i} className="suggested-query-chip" onClick={() => onSelect(q)}>
          {q}
        </button>
      ))}
    </div>
  );
}

export default function AgentUI() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'agent',
      text: 'Hello! I am the Ontology Advisor — your unified supply chain analytics agent powered by Snowflake Cortex. Ask me questions about sales, production, inventory, customers, or any cross-domain topic.',
      toolCalls: [],
      tableData: null,
      suggestedQueries: [],
    }
  ]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const submitQuestion = async (question) => {
    if (!question.trim() || loading) return;

    const userMsg = { id: Date.now(), sender: 'user', text: question, toolCalls: [], tableData: null, suggestedQueries: [] };
    setMessages(prev => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const result = await sendChatMessage(question);
      const agentMsg = {
        id: Date.now() + 1,
        sender: 'agent',
        text: result.response,
        toolCalls: result.tool_calls || [],
        tableData: result.table_data || null,
        suggestedQueries: result.suggested_queries || [],
        agentName: result.agent_name || '',
      };
      setMessages(prev => [...prev, agentMsg]);
    } catch {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'agent',
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        toolCalls: [],
        tableData: null,
        suggestedQueries: [],
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitQuestion(query);
  };

  return (
    <div className="agent-ui-container">
      <div className="agent-header">
        <div className="agent-header-top">
          <div>
            <h2>Speak with Data</h2>
            <p>Ontology Advisor — Cortex Agent powered analytics with semantic views</p>
          </div>
          <span className="agent-badge-header">Ontology Advisor</span>
        </div>
      </div>

      <div className="chat-window">
        {messages.map(msg => (
          <div key={msg.id} className={`chat-bubble-wrapper ${msg.sender}`}>
            <div className="chat-avatar">
              {msg.sender === 'agent' ? <Bot size={20} /> : <User size={20} />}
            </div>
            <div className="chat-bubble-content">
              {msg.agentName && msg.sender === 'agent' && (
                <span className="agent-badge">{msg.agentName}</span>
              )}
              {msg.toolCalls && msg.toolCalls.length > 0 && (
                <div className="tool-calls-section">
                  <span className="tool-calls-label">
                    <Database size={12} /> {msg.toolCalls.length} tool{msg.toolCalls.length > 1 ? 's' : ''} executed
                  </span>
                  {msg.toolCalls.map((tc, i) => (
                    <ToolCallCard key={i} tool={tc} />
                  ))}
                </div>
              )}
              <div className={`chat-bubble ${msg.sender}`}>
                {msg.text}
              </div>
              {msg.tableData && <DataTable tableData={msg.tableData} />}
              {msg.suggestedQueries && msg.suggestedQueries.length > 0 && (
                <SuggestedQueries queries={msg.suggestedQueries} onSelect={submitQuestion} />
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-bubble-wrapper agent">
            <div className="chat-avatar"><Bot size={20} /></div>
            <div className="chat-bubble-content">
              <div className="chat-bubble agent typing-indicator">
                <Loader2 size={16} className="spinning" /> Ontology Advisor is querying data...
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form className="chat-input-wrapper" onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask the Ontology Advisor about your supply chain data..."
          className="chat-input"
          disabled={loading}
        />
        <button type="submit" className="chat-submit" disabled={!query.trim() || loading}>
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
