import { useState } from 'react'
import Header from '../components/Header.jsx'
import ChatWindow from '../components/ChatWindow.jsx'
import { sendCodingMessage } from '../services/api.js'

export default function CodingAgent() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('')
  const [conversationId, setConversationId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSend = async () => {
    if (!input.trim()) return
    const userMessage = input.trim()
    const displayContent = code.trim() ? `${userMessage}\n\n\`\`\`${language}\n${code}\n\`\`\`` : userMessage
    setMessages((prev) => [...prev, { role: 'user', content: displayContent }])
    setInput('')
    setLoading(true)
    setError('')
    try {
      const { reply, conversation_id } = await sendCodingMessage(userMessage, code, language, conversationId)
      setConversationId(conversation_id)
      setMessages((prev) => [...prev, { role: 'assistant', content: reply }])
      setCode('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Header title="Coding Agent" subtitle="Paste code and describe the problem — get an explanation or a fix." />
      <ChatWindow
        messages={messages}
        input={input}
        setInput={setInput}
        onSend={handleSend}
        loading={loading}
        placeholder="Describe the bug or question…"
        extraControls={
          <div className="flex gap-2 py-2">
            <input
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              placeholder="language (optional, e.g. python)"
              className="w-48 bg-white/5 border border-nexus-border rounded-md px-2 py-1.5 text-xs text-gray-300 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-nexus-teal/40"
            />
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              rows={2}
              placeholder="Paste code here (optional)"
              className="flex-1 bg-white/5 border border-nexus-border rounded-md px-2 py-1.5 text-xs font-mono text-gray-300 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-nexus-teal/40"
            />
          </div>
        }
      />
      {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
    </div>
  )
}
