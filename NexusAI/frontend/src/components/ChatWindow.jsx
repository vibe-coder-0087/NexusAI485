/**
 * Shared chat UI used by ChatAgent and CodingAgent pages: a scrolling
 * message list plus a composer. Keeps both agent pages thin.
 */
export default function ChatWindow({ messages, input, setInput, onSend, loading, placeholder, extraControls }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSend()
    }
  }

  return (
    <div className="flex flex-col h-[70vh] border border-nexus-border rounded-xl bg-nexus-panel/40 overflow-hidden">
      <div className="flex-1 overflow-y-auto scrollbar-thin px-5 py-5 space-y-4">
        {messages.length === 0 && (
          <div className="text-sm text-gray-600 italic">Send a message to get started.</div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2.5 text-sm whitespace-pre-wrap leading-relaxed ${
                m.role === 'user'
                  ? 'bg-nexus-teal/15 text-white ring-1 ring-nexus-teal/25'
                  : 'bg-white/5 text-gray-300'
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
        {loading && <div className="text-xs text-gray-500">NexusAI is thinking…</div>}
      </div>

      {extraControls && <div className="px-5 pt-2 border-t border-nexus-border">{extraControls}</div>}

      <div className="border-t border-nexus-border p-3 flex gap-2 items-end">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder={placeholder}
          className="flex-1 resize-none bg-transparent text-sm text-gray-200 placeholder-gray-600 focus:outline-none px-3 py-2"
        />
        <button
          onClick={onSend}
          disabled={loading || !input.trim()}
          className="px-4 py-2 rounded-lg bg-nexus-teal text-nexus-bg text-sm font-medium disabled:opacity-30 disabled:cursor-not-allowed hover:brightness-110 transition"
        >
          Send
        </button>
      </div>
    </div>
  )
}
