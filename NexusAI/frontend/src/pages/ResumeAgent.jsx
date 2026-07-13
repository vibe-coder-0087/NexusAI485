import { useState } from 'react'
import Header from '../components/Header.jsx'
import { analyzeResume } from '../services/api.js'

export default function ResumeAgent() {
  const [file, setFile] = useState(null)
  const [targetRole, setTargetRole] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await analyzeResume(file, targetRole)
      setResult(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Header title="Resume Agent" subtitle="Upload a resume (.pdf, .docx, .txt) for direct, specific feedback." />

      <form onSubmit={handleSubmit} className="border border-nexus-border rounded-xl bg-nexus-panel/40 p-5 space-y-4 mb-6">
        <div>
          <label className="text-xs text-gray-500 block mb-1">Resume file *</label>
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={(e) => setFile(e.target.files[0] || null)}
            className="w-full text-sm text-gray-400 file:mr-3 file:py-2 file:px-3 file:rounded-md file:border-0 file:text-xs file:bg-nexus-teal/15 file:text-nexus-teal hover:file:bg-nexus-teal/25"
          />
        </div>
        <div>
          <label className="text-xs text-gray-500 block mb-1">Target role (optional)</label>
          <input
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
            placeholder="e.g. Frontend Engineering Internship"
            className="w-full bg-white/5 border border-nexus-border rounded-md px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-nexus-teal/40"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !file}
          className="px-5 py-2 rounded-lg bg-nexus-teal text-nexus-bg text-sm font-medium disabled:opacity-30 hover:brightness-110 transition"
        >
          {loading ? 'Analyzing…' : 'Analyze resume'}
        </button>
      </form>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {result && (
        <div className="border border-nexus-border rounded-xl bg-nexus-panel/40 p-5">
          <div className="text-xs text-gray-500 mb-3">Feedback on {result.filename}</div>
          <div className="text-sm text-gray-300 whitespace-pre-wrap leading-relaxed">{result.feedback}</div>
        </div>
      )}
    </div>
  )
}
