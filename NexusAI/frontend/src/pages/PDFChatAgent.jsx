import { useState } from 'react'
import Header from '../components/Header.jsx'
import ChatWindow from '../components/ChatWindow.jsx'
import { uploadPDF, askPDFQuestion } from '../services/api.js'

export default function PDFChatAgent() {
  const [file, setFile] = useState(null)
  const [conversationId, setConversationId] = useState(null)
  const [filename, setFilename] = useState('')
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [uploading, setUploading] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setError('')
    try {
      const res = await uploadPDF(file)
      setConversationId(res.conversation_id)
      setFilename(res.filename)
      setMessages([])
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  const handleSend = async () => {
    if (!input.trim() || !conversationId) return
    const question = input.trim()
    setMessages((prev) => [...prev, { role: 'user', content: question }])
    setInput('')
    setLoading(true)
    setError('')
    try {
      const { reply } = await askPDFQuestion(conversationId, question)
      setMessages((prev) => [...prev, { role: 'assistant', content: reply }])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Header title="PDF Chat Agent" subtitle="Upload a PDF, then ask questions grounded in its content." />

      <div className="border border-nexus-border rounded-xl bg-nexus-panel/40 p-5 mb-6 flex flex-wrap items-center gap-3">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0] || null)}
          className="text-sm text-gray-400 file:mr-3 file:py-2 file:px-3 file:rounded-md file:border-0 file:text-xs file:bg-nexus-teal/15 file:text-nexus-teal hover:file:bg-nexus-teal/25"
        />
        <button
          onClick={handleUpload}
          disabled={uploading || !file}
          className="px-4 py-2 rounded-lg bg-nexus-teal text-nexus-bg text-sm font-medium disabled:opacity-30 hover:brightness-110 transition"
        >
          {uploading ? 'Uploading…' : 'Upload PDF'}
        </button>
        {filename && <span className="text-xs text-gray-500">Loaded: {filename}</span>}
      </div>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      <ChatWindow
        messages={messages}
        input={input}
        setInput={setInput}
        onSend={handleSend}
        loading={loading}
        placeholder={conversationId ? 'Ask something about the document…' : 'Upload a PDF first'}
      />
    </div>
  )
}
