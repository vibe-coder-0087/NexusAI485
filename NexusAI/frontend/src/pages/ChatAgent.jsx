import { useState } from 'react'
import Header from '../components/Header.jsx'
import ChatWindow from '../components/ChatWindow.jsx'
import { sendChatMessage } from '../services/api.js'

export default function ChatAgent() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [conversationId, setConversationId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSend = async () => {
    if (!input.trim()) return
    const userMessage = input.trim()
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setInput('')
    setLoading(true)
    setError('')
    try {
      const { reply, conversation_id } = await sendChatMessage(userMessage, conversationId)
      setConversationId(conversation_id)
      setMessages((prev) => [...prev, { role: 'assistant', content: reply }])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Header title="Chat Agent" subtitle="Ask anything about academics, career decisions, or student life." />
      <ChatWindow
        messages={messages}
        input={input}
        setInput={setInput}
        onSend={handleSend}
        loading={loading}
        placeholder="Ask NexusAI something…"
      />
      {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
    </div>
  )
}
