import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout.jsx'
import Dashboard from './pages/Dashboard.jsx'
import ChatAgent from './pages/ChatAgent.jsx'
import CodingAgent from './pages/CodingAgent.jsx'
import StudyAgent from './pages/StudyAgent.jsx'
import ResumeAgent from './pages/ResumeAgent.jsx'
import PDFChatAgent from './pages/PDFChatAgent.jsx'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/chat" element={<ChatAgent />} />
        <Route path="/coding" element={<CodingAgent />} />
        <Route path="/study" element={<StudyAgent />} />
        <Route path="/resume" element={<ResumeAgent />} />
        <Route path="/pdf-chat" element={<PDFChatAgent />} />
      </Routes>
    </Layout>
  )
}
