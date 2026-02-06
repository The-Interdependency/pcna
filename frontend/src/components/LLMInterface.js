import React, { useState } from 'react';
import axios from 'axios';

const LLMInterface = ({ backendUrl }) => {
  const [prompt, setPrompt] = useState('');
  const [provider, setProvider] = useState('openai');
  const [model, setModel] = useState('gpt-5.2');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [providerStatus, setProviderStatus] = useState(null);

  const providers = {
    openai: ['gpt-5.2', 'gpt-5.1', 'gpt-5', 'gpt-5-mini'],
    anthropic: ['claude-4-sonnet-20250514', 'claude-sonnet-4-5-20250929', 'claude-opus-4-5-20251101'],
    gemini: ['gemini-2.5-pro', 'gemini-3-flash-preview', 'gemini-2.5-flash']
  };

  const sendMessage = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    const userMessage = { role: 'user', content: prompt, timestamp: new Date().toISOString() };
    setChatHistory(prev => [...prev, userMessage]);
    setPrompt('');

    try {
      const response = await axios.post(`${backendUrl}/api/llm/chat`, {
        prompt,
        provider,
        model
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        provider: response.data.provider,
        model: response.data.model,
        timestamp: new Date().toISOString()
      };
      setChatHistory(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'error',
        content: `Error: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date().toISOString()
      };
      setChatHistory(prev => [...prev, errorMessage]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearHistory = () => {
    setChatHistory([]);
  };

  return (
    <div className="space-y-6" data-testid="llm-interface">
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <h2 className="text-2xl font-bold mb-4">🤖 LLM Chat Interface</h2>
        <p className="text-slate-400 mb-4">
          Hot-swappable multi-provider LLM chat with automatic fallback
        </p>

        {/* Provider Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Provider</label>
            <select
              value={provider}
              onChange={(e) => {
                setProvider(e.target.value);
                setModel(providers[e.target.value][0]);
              }}
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-2 focus:ring-2 focus:ring-pcna-primary outline-none"
            >
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic (Claude)</option>
              <option value="gemini">Google Gemini</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Model</label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full bg-slate-700 text-white rounded-lg px-4 py-2 focus:ring-2 focus:ring-pcna-primary outline-none"
            >
              {providers[provider].map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Chat History */}
        <div className="bg-slate-900/50 rounded-lg p-4 h-96 overflow-y-auto mb-4 space-y-4">
          {chatHistory.length === 0 ? (
            <div className="h-full flex items-center justify-center text-slate-500">
              <div className="text-center">
                <div className="text-4xl mb-4">💬</div>
                <p>Start a conversation with the LLM</p>
                <p className="text-sm mt-2">Using Emergent Universal Key</p>
              </div>
            </div>
          ) : (
            chatHistory.map((message, idx) => (
              <div
                key={idx}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-pcna-primary text-white'
                      : message.role === 'error'
                      ? 'bg-red-500/20 text-red-400 border border-red-500'
                      : 'bg-slate-700 text-white'
                  }`}
                >
                  {message.role === 'assistant' && (
                    <div className="text-xs text-slate-400 mb-2">
                      {message.provider} / {message.model}
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">{message.content}</div>
                  <div className="text-xs text-slate-400 mt-2">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-slate-700 rounded-lg p-4">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-pcna-primary rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-pcna-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-pcna-primary rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="flex space-x-2">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message... (Shift+Enter for new line)"
            className="flex-1 bg-slate-700 text-white rounded-lg px-4 py-3 focus:ring-2 focus:ring-pcna-primary outline-none resize-none"
            rows="3"
          />
          <div className="flex flex-col space-y-2">
            <button
              onClick={sendMessage}
              disabled={loading || !prompt.trim()}
              className="px-6 py-3 bg-gradient-to-r from-pcna-primary to-pcna-secondary text-white rounded-lg hover:opacity-90 disabled:opacity-50 font-medium"
              data-testid="send-message-btn"
            >
              {loading ? '⏳' : '🚀'} Send
            </button>
            <button
              onClick={clearHistory}
              className="px-6 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600"
            >
              🗑️ Clear
            </button>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-bold mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={() => setPrompt('Analyze the current PCNA system health and provide optimization recommendations.')}
            className="bg-slate-700 hover:bg-slate-600 text-white rounded-lg p-3 text-left transition-all"
          >
            <div className="font-medium">📊 System Analysis</div>
            <div className="text-xs text-slate-400 mt-1">Analyze system health</div>
          </button>
          <button
            onClick={() => setPrompt('Generate a professional outreach message to an AI researcher interested in neural architectures.')}
            className="bg-slate-700 hover:bg-slate-600 text-white rounded-lg p-3 text-left transition-all"
          >
            <div className="font-medium">📨 Researcher Outreach</div>
            <div className="text-xs text-slate-400 mt-1">Generate outreach message</div>
          </button>
          <button
            onClick={() => setPrompt('Explain EDCM (Entropy Dissonance Constraint Management) in simple terms for a general audience.')}
            className="bg-slate-700 hover:bg-slate-600 text-white rounded-lg p-3 text-left transition-all"
          >
            <div className="font-medium">📝 EDCM Explainer</div>
            <div className="text-xs text-slate-400 mt-1">Explain EDCM concepts</div>
          </button>
        </div>
      </div>

      {/* Provider Info */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-bold mb-4">🔑 Authentication</h3>
        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
          <div className="flex items-center space-x-2 text-green-400">
            <span>✅</span>
            <span className="font-medium">Using Emergent Universal Key</span>
          </div>
          <p className="text-sm text-slate-400 mt-2">
            This system uses the Emergent Universal Key which works across OpenAI, Anthropic, and Google Gemini providers.
            Automatic fallback ensures high availability.
          </p>
        </div>
      </div>
    </div>
  );
};

export default LLMInterface;
