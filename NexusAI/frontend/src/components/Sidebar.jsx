import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard', icon: '⌂', end: true },
  { to: '/chat', label: 'Chat Agent', icon: '💬' },
  { to: '/coding', label: 'Coding Agent', icon: '⌨' },
  { to: '/study', label: 'Study Agent', icon: '📘' },
  { to: '/resume', label: 'Resume Agent', icon: '📄' },
  { to: '/pdf-chat', label: 'PDF Chat Agent', icon: '📑' },
]

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 border-r border-nexus-border bg-nexus-panel/60 h-screen sticky top-0 flex flex-col">
      <div className="px-5 py-6">
        <div className="font-display font-bold text-lg text-white tracking-tight">
          Nexus<span className="text-nexus-teal">AI</span>
        </div>
        <div className="text-[11px] text-gray-500 mt-1">student success, in one place</div>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                isActive
                  ? 'bg-nexus-teal/10 text-white ring-1 ring-nexus-teal/30'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <span className="text-base opacity-80">{l.icon}</span>
            {l.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-5 py-5 text-[11px] text-gray-600 border-t border-nexus-border">
        v0.1 · MVP build
      </div>
    </aside>
  )
}
