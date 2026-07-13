import { useState } from 'react'
import Header from '../components/Header.jsx'
import { generateStudyPlan } from '../services/api.js'

export default function StudyAgent() {
  const [goal, setGoal] = useState('')
  const [subjects, setSubjects] = useState('')
  const [hoursPerDay, setHoursPerDay] = useState('')
  const [deadline, setDeadline] = useState('')
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!goal.trim()) return
    setLoading(true)
    setError('')
    setPlan(null)
    try {
      const result = await generateStudyPlan({ goal, subjects, hoursPerDay, deadline })
      setPlan(result.plan)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Header title="Study Agent" subtitle="Describe your goal and NexusAI will build a day-by-day study plan." />

      <form onSubmit={handleSubmit} className="border border-nexus-border rounded-xl bg-nexus-panel/40 p-5 space-y-4 mb-6">
        <div>
          <label className="text-xs text-gray-500 block mb-1">Goal *</label>
          <input
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g. Pass my Data Structures final"
            className="w-full bg-white/5 border border-nexus-border rounded-md px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-nexus-teal/40"
          />
        </div>
        <div className="grid sm:grid-cols-3 gap-4">
          <div>
            <label className="text-xs text-gray-500 block mb-1">Subjects / topics</label>
            <input
              value={subjects}
              onChange={(e) => setSubjects(e.target.value)}
              placeholder="Trees, graphs, DP"
              className="w-full bg-white/5 border border-nexus-border rounded-md px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-nexus-teal/40"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 block mb-1">Hours/day available</label>
            <input
              value={hoursPerDay}
              onChange={(e) => setHoursPerDay(e.target.value)}
              placeholder="2"
              className="w-full bg-white/5 border border-nexus-border rounded-md px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-nexus-teal/40"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 block mb-1">Deadline</label>
            <input
              value={deadline}
              onChange={(e) => setDeadline(e.target.value)}
              placeholder="in 7 days"
              className="w-full bg-white/5 border border-nexus-border rounded-md px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-nexus-teal/40"
            />
          </div>
        </div>
        <button
          type="submit"
          disabled={loading || !goal.trim()}
          className="px-5 py-2 rounded-lg bg-nexus-teal text-nexus-bg text-sm font-medium disabled:opacity-30 hover:brightness-110 transition"
        >
          {loading ? 'Generating…' : 'Generate plan'}
        </button>
      </form>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {plan && (
        <div className="border border-nexus-border rounded-xl bg-nexus-panel/40 p-5">
          <p className="text-sm text-gray-300 mb-4">{plan.summary}</p>
          <div className="space-y-3">
            {plan.days?.map((d, i) => (
              <div key={i} className="border border-nexus-border rounded-lg p-4 bg-white/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-display font-semibold text-white text-sm">{d.day}</span>
                  <span className="text-xs text-gray-500">{d.duration_minutes} min</span>
                </div>
                <div className="text-xs text-nexus-teal mb-1">{d.focus}</div>
                <ul className="list-disc list-inside text-sm text-gray-400 space-y-0.5">
                  {d.tasks?.map((t, j) => <li key={j}>{t}</li>)}
                </ul>
              </div>
            ))}
          </div>
          {plan.tips?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-nexus-border">
              <div className="text-xs text-gray-500 mb-2">Tips</div>
              <ul className="list-disc list-inside text-sm text-gray-400 space-y-0.5">
                {plan.tips.map((t, i) => <li key={i}>{t}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
