import React, { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar.jsx'
import Dashboard from './pages/Dashboard.jsx'
import AIAssistant from './pages/AIAssistant.jsx'
import ContentGenerator from './pages/ContentGenerator.jsx'
import Trends from './pages/Trends.jsx'
import Sentiment from './pages/Sentiment.jsx'
import Competitors from './pages/Competitors.jsx'
import Campaigns from './pages/Campaigns.jsx'
import Settings from './pages/Settings.jsx'
import AgentWorkflow from './components/AgentWorkflow.jsx'
import { api } from './hooks/useApi.jsx'
import { Zap } from 'lucide-react'

const PAGE_HEADERS = {
  dashboard:   { title: '📊 Social Media Pulse',     subtitle: 'Unified analytics powered by IBM Granite AI' },
  assistant:   { title: '🤖 AI Assistant',           subtitle: 'Chat with your IBM Granite-powered social media agent' },
  generator:   { title: '✍️ Content Generator',      subtitle: 'Generate AI-optimized posts, captions, and campaigns' },
  trends:      { title: '📈 Trend Intelligence',     subtitle: 'Emerging hashtags, viral topics, and forecasts' },
  sentiment:   { title: '💬 Sentiment Analysis',     subtitle: 'Audience mood tracking and comment intelligence' },
  competitors: { title: '🏆 Competitor Intelligence', subtitle: 'Competitive landscape analysis and gap identification' },
  campaigns:   { title: '🎯 Campaign Manager',       subtitle: 'Campaign performance, AI recommendations, and scheduling' },
  workflow:    { title: '🔄 Agentic Workflow',       subtitle: 'Visualize and run the full IBM Granite agent pipeline' },
  settings:    { title: '⚙️ Settings',               subtitle: 'Configuration, architecture, and system status' },
};

function App() {
  const [page, setPage] = useState('dashboard');
  const [graniteStatus, setGraniteStatus] = useState('checking');

  useEffect(() => {
    api.health()
      .then(h => setGraniteStatus(h.granite_mode === 'ibm_watsonx_ai' ? 'live' : 'demo'))
      .catch(() => setGraniteStatus('demo'));
  }, []);

  const renderPage = () => {
    switch (page) {
      case 'dashboard':   return <Dashboard />;
      case 'assistant':   return <AIAssistant />;
      case 'generator':   return <ContentGenerator />;
      case 'trends':      return <Trends />;
      case 'sentiment':   return <Sentiment />;
      case 'competitors': return <Competitors />;
      case 'campaigns':   return <Campaigns />;
      case 'workflow':    return <AgentWorkflow />;
      case 'settings':    return <Settings />;
      default:            return <Dashboard />;
    }
  };

  const header = PAGE_HEADERS[page] || PAGE_HEADERS.dashboard;
  const isFullHeight = page === 'assistant';

  return (
    <div className="app-layout">
      <Sidebar activePage={page} onNavigate={setPage} graniteStatus={graniteStatus} />

      <div className="main-content">
        {/* Page header */}
        <div className="page-header">
          <div>
            <div className="page-title">{header.title}</div>
            <div className="page-subtitle">{header.subtitle}</div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            {/* Workflow button */}
            <button
              className={`btn btn-secondary`}
              onClick={() => setPage('workflow')}
              title="View agentic workflow"
              style={{ fontSize: 12, padding: '6px 12px' }}
            >
              <Zap size={13} /> Agents
            </button>

            {/* IBM Badge */}
            <div style={{
              background: '#1e293b',
              border: '1px solid #293548',
              borderRadius: 8,
              padding: '6px 12px',
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              fontSize: 12,
              color: '#94a3b8',
            }}>
              <div style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: graniteStatus === 'live' ? '#34d399' : '#fbbf24',
                boxShadow: `0 0 6px ${graniteStatus === 'live' ? '#34d399' : '#fbbf24'}`,
              }} />
              <span>IBM Granite {graniteStatus === 'live' ? 'Live' : 'Demo'}</span>
            </div>
          </div>
        </div>

        {/* Page content */}
        {isFullHeight ? renderPage() : (
          <div style={{ flex: 1, overflowY: 'auto' }}>
            {renderPage()}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
