const BASE_URL = '/api';

async function fetchJSON(url) {
  const response = await fetch(`${BASE_URL}${url}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

async function postJSON(url, body) {
  const response = await fetch(`${BASE_URL}${url}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

export function getPersonas() {
  return fetchJSON('/personas');
}

export function getPersonaDashboard(personaId) {
  return fetchJSON(`/personas/${personaId}/dashboard`);
}

export function getOntology() {
  return fetchJSON('/ontology');
}

export function getHealth() {
  return fetchJSON('/health');
}

export function sendChatMessage(message, conversationHistory = null) {
  return postJSON('/ai/chat', {
    message,
    conversation_history: conversationHistory,
  });
}

export function getAvailableAgents() {
  return fetchJSON('/ai/agents');
}

export function getStockRisk() {
  return fetchJSON('/ai/stock-risk');
}

export function getQualitySentiment() {
  return fetchJSON('/ai/quality-sentiment');
}

export function getAiInsights(personaId) {
  return fetchJSON(`/ai/insights/${personaId}`);
}
