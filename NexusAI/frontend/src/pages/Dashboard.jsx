import { Link } from 'react-router-dom'
import Header from '../components/Header.jsx'

const agents = [
  { to: '/chat', name: 'Chat Agent', desc: 'Ask career, academic, or general student-life questions.', icon: '💬' },
  { to: '/coding', name: 'Coding Agent', desc: 'Paste code and get debugging help or explanations.', icon: '⌨' },
  { to: '/study', name: 'Study Agent', desc: 'Turn a goal and deadline into a day-by-day study plan.', icon: '📘' },
  { to: '/resume', name: 'Resume Agent', desc: 'Upload a resume and get specific, actionable feedback.', icon: '📄' },
  { to: '/pdf-chat', name: 'PDF Chat Agent', desc: 'Upload a PDF and ask questions grounded in its content.', icon: '📑' },
]

export default function Dashboard() {
  return (
    <div>
      <Header
        title="Welcome to NexusAI"
        subtitle="One platform for learning, career growth, and AI guidance — from first semester to first job."
      />
      <div className="grid sm:grid-cols-2 gap-4">
        {agents.map((a) => (
          <Link
            key={a.to}
            to={a.to}
            className="group border border-nexus-border rounded-xl bg-nexus-panel/40 p-5 hover:border-nexus-teal/40 hover:bg-nexus-panel transition-colors"
          >
            <div className="text-2xl mb-3">{a.icon}</div>
            <div className="font-display font-semibold text-white mb-1 group-hover:text-nexus-teal transition-colors">
              {a.name}
            </div>
            <div className="text-sm text-gray-500">{a.desc}</div>
          </Link>
        ))}
      </div>
    </div>
  )
}
