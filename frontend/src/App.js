import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';

// Import components
import TopologyVisualization from './components/TopologyVisualization';
import SystemHealthDashboard from './components/SystemHealthDashboard';
import LLMInterface from './components/LLMInterface';
import EDCMArtifacts from './components/EDCMArtifacts';
import SMSConsole from './components/SMSConsole';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8001';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [systemState, setSystemState] = useState(null);
  const [websocket, setWebsocket] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  // Initialize WebSocket connection
  useEffect(() => {
    const ws = new WebSocket(`${WS_URL}/ws`);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
      setWebsocket(ws);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setSystemState(data);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnectionStatus('disconnected');
      // Attempt to reconnect after 5 seconds
      setTimeout(() => {
        window.location.reload();
      }, 5000);
    };
    
    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'topology', label: 'Topology', icon: '🌐' },
    { id: 'llm', label: 'LLM Chat', icon: '💬' },
    { id: 'edcm', label: 'EDCM Artifacts', icon: '📈' },
    { id: 'sms', label: 'SMS Console', icon: '📱' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-pcna-dark via-slate-800 to-pcna-dark">
      {/* Header */}
      <header className="bg-slate-900/50 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="text-3xl font-bold bg-gradient-to-r from-pcna-primary to-pcna-secondary bg-clip-text text-transparent">
                PCNA Agent System
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <span className={`w-2 h-2 rounded-full ${
                  connectionStatus === 'connected' ? 'bg-green-500 pulse-glow' :
                  connectionStatus === 'error' ? 'bg-red-500' :
                  'bg-yellow-500'
                }`}></span>
                <span className="text-slate-400">
                  {connectionStatus === 'connected' ? 'Live' : 
                   connectionStatus === 'error' ? 'Error' : 
                   'Connecting...'}
                </span>
              </div>
            </div>
            
            {systemState && (
              <div className="flex items-center space-x-6 text-sm">
                <div className="flex flex-col items-end">
                  <span className="text-slate-400">System Health</span>
                  <span className={`font-bold ${
                    systemState.system_health?.status === 'HEALTHY' ? 'text-green-400' :
                    systemState.system_health?.status === 'DEGRADED' ? 'text-yellow-400' :
                    'text-red-400'
                  }`}>
                    {systemState.system_health?.status || 'UNKNOWN'}
                  </span>
                </div>
                <div className="flex flex-col items-end">
                  <span className="text-slate-400">Active Seeds</span>
                  <span className="font-bold text-pcna-primary">
                    {systemState.system_health?.total_seeds || 0}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-slate-900/30 backdrop-blur-sm border-b border-slate-700">
        <div className="container mx-auto px-6">
          <div className="flex space-x-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-pcna-primary to-pcna-secondary text-white border-b-2 border-pcna-accent'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="fade-in">
          {activeTab === 'dashboard' && (
            <SystemHealthDashboard systemState={systemState} backendUrl={BACKEND_URL} />
          )}
          {activeTab === 'topology' && (
            <TopologyVisualization systemState={systemState} backendUrl={BACKEND_URL} />
          )}
          {activeTab === 'llm' && (
            <LLMInterface backendUrl={BACKEND_URL} />
          )}
          {activeTab === 'edcm' && (
            <EDCMArtifacts backendUrl={BACKEND_URL} />
          )}
          {activeTab === 'sms' && (
            <SMSConsole backendUrl={BACKEND_URL} />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-900/30 border-t border-slate-700 mt-12">
        <div className="container mx-auto px-6 py-6">
          <div className="flex justify-between items-center text-sm text-slate-400">
            <div>
              <p>PCNA v1.0 - Prime Circular Neural Architecture</p>
              <p className="text-xs mt-1">Trauma-informed, transparent, harm reduction focused</p>
            </div>
            <div className="text-right">
              <p>Interdependent Way Project</p>
              <p className="text-xs mt-1">Building better AI-human interactions</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
