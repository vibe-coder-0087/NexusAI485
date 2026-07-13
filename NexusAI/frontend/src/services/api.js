/**
 * Thin fetch wrapper around the NexusAI backend.
 * One function per endpoint - pages import from here instead of calling
 * fetch() directly, so the base URL and error handling live in one place.
 */
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: options.body instanceof FormData ? undefined : { 'Content-Type': 'application/json' },
    ...options,
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(data.error || `Request failed (${res.status})`)
  }
  return data
}

// --- Chat Agent ---
export const sendChatMessage = (message, conversationId) =>
  request('/api/chat/message', {
    method: 'POST',
    body: JSON.stringify({ message, conversation_id: conversationId }),
  })

// --- Coding Agent ---
export const sendCodingMessage = (message, code, language, conversationId) =>
  request('/api/coding/message', {
    method: 'POST',
    body: JSON.stringify({ message, code, language, conversation_id: conversationId }),
  })

// --- Study Agent ---
export const generateStudyPlan = ({ goal, subjects, hoursPerDay, deadline }) =>
  request('/api/study/plan', {
    method: 'POST',
    body: JSON.stringify({ goal, subjects, hours_per_day: hoursPerDay, deadline }),
  })

// --- Resume Agent ---
export const analyzeResume = (file, targetRole) => {
  const formData = new FormData()
  formData.append('resume', file)
  if (targetRole) formData.append('target_role', targetRole)
  return request('/api/resume/analyze', { method: 'POST', body: formData })
}

// --- PDF Chat Agent ---
export const uploadPDF = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request('/api/pdf-chat/upload', { method: 'POST', body: formData })
}

export const askPDFQuestion = (conversationId, question) =>
  request('/api/pdf-chat/ask', {
    method: 'POST',
    body: JSON.stringify({ conversation_id: conversationId, question }),
  })

// --- Health ---
export const checkHealth = () => request('/api/health')
