import Sidebar from './Sidebar.jsx'

export default function Layout({ children }) {
  return (
    <div className="flex min-h-screen bg-nexus-bg text-gray-200">
      <Sidebar />
      <main className="flex-1 px-8 py-8 max-w-5xl">{children}</main>
    </div>
  )
}
