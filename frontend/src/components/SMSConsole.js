import React, { useState } from 'react';
import axios from 'axios';

const SMSConsole = ({ backendUrl }) => {
  const [command, setCommand] = useState('');
  const [consoleHistory, setConsoleHistory] = useState([
    {
      type: 'system',
      content: 'SMS Console initialized in MOCK mode. Messages will be logged only.',
      timestamp: new Date().toISOString()
    }
  ]);
  const [loading, setLoading] = useState(false);

  const sendCommand = async () => {
    if (!command.trim()) return;

    setLoading(true);
    const userCommand = {
      type: 'user',
      content: command,
      timestamp: new Date().toISOString()
    };
    setConsoleHistory(prev => [...prev, userCommand]);

    try {
      const response = await axios.post(`${backendUrl}/api/sms/command`, {
        command: command
      });

      const systemResponse = {
        type: 'response',
        content: response.data.response,
        timestamp: new Date().toISOString()
      };
      setConsoleHistory(prev => [...prev, systemResponse]);
    } catch (error) {
      const errorResponse = {
        type: 'error',
        content: `Error: ${error.response?.data?.detail || error.message}`,
        timestamp: new Date().toISOString()
      };
      setConsoleHistory(prev => [...prev, errorResponse]);
    }

    setCommand('');
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendCommand();
    }
  };

  const quickCommands = ['STATUS', 'HEALTH', 'LAST_TICK', 'HELP'];

  return (
    <div className="space-y-6" data-testid="sms-console">
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <h2 className="text-2xl font-bold mb-2">📱 SMS Console</h2>
        <p className="text-slate-400 mb-4">
          Simulate SMS commands and check-ins (Mock mode for development)
        </p>

        {/* Mock Mode Notice */}
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-6">
          <div className="flex items-center space-x-2 text-yellow-400">
            <span>⚠️</span>
            <span className="font-medium">Mock Mode Active</span>
          </div>
          <p className="text-sm text-slate-400 mt-2">
            SMS service is running in mock mode. Messages are logged to console instead of sending real SMS.
            When ready, configure Twilio API keys to enable real SMS functionality.
          </p>
        </div>

        {/* Console Display */}
        <div className="bg-slate-900/50 rounded-lg p-4 h-96 overflow-y-auto mb-4 font-mono text-sm space-y-3">
          {consoleHistory.map((entry, idx) => (
            <div key={idx} className="fade-in">
              <div className="text-xs text-slate-500 mb-1">
                {new Date(entry.timestamp).toLocaleTimeString()}
              </div>
              <div
                className={`p-3 rounded-lg ${
                  entry.type === 'user'
                    ? 'bg-pcna-primary/20 text-white ml-12'
                    : entry.type === 'error'
                    ? 'bg-red-500/20 text-red-400'
                    : entry.type === 'system'
                    ? 'bg-blue-500/20 text-blue-400'
                    : 'bg-slate-700 text-white'
                }`}
              >
                <div className="whitespace-pre-wrap">{entry.content}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex items-center space-x-2 text-slate-400">
              <div className="animate-spin">⚙️</div>
              <span>Processing...</span>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="flex space-x-2 mb-4">
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter SMS command..."
            className="flex-1 bg-slate-700 text-white rounded-lg px-4 py-3 focus:ring-2 focus:ring-pcna-primary outline-none"
          />
          <button
            onClick={sendCommand}
            disabled={loading || !command.trim()}
            className="px-6 py-3 bg-gradient-to-r from-pcna-primary to-pcna-secondary text-white rounded-lg hover:opacity-90 disabled:opacity-50 font-medium"
            data-testid="send-command-btn"
          >
            Send
          </button>
        </div>

        {/* Quick Commands */}
        <div>
          <div className="text-sm text-slate-400 mb-2">Quick Commands:</div>
          <div className="flex flex-wrap gap-2">
            {quickCommands.map((cmd) => (
              <button
                key={cmd}
                onClick={() => setCommand(cmd)}
                className="px-3 py-1 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm transition-all"
              >
                {cmd}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* SMS Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold mb-4">📤 Outbound Features</h3>
          <div className="space-y-3 text-sm">
            <div className="flex items-start space-x-3">
              <span className="text-green-400">✓</span>
              <div>
                <div className="font-medium">Hourly Check-ins</div>
                <div className="text-slate-400">Automated system health reports</div>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-green-400">✓</span>
              <div>
                <div className="font-medium">Critical Alerts</div>
                <div className="text-slate-400">Immediate notifications on system degradation</div>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <span className="text-green-400">✓</span>
              <div>
                <div className="font-medium">EDCM Reports</div>
                <div className="text-slate-400">Automated artifact generation alerts</div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold mb-4">📥 Inbound Commands</h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-300">STATUS</span>
              <span className="text-slate-500">Get system status</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-300">HEALTH</span>
              <span className="text-slate-500">Detailed health metrics</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-300">LAST_TICK</span>
              <span className="text-slate-500">Last tick information</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-300">HELP</span>
              <span className="text-slate-500">Show available commands</span>
            </div>
          </div>
        </div>
      </div>

      {/* Setup Instructions */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-bold mb-4">🔧 Production Setup (Twilio)</h3>
        <div className="space-y-3 text-sm text-slate-400">
          <p>To enable real SMS functionality:</p>
          <ol className="list-decimal list-inside space-y-2 ml-4">
            <li>Sign up for a Twilio account and get API credentials</li>
            <li>Add <code className="bg-slate-900 px-2 py-1 rounded text-pcna-primary">TWILIO_ACCOUNT_SID</code> to backend/.env</li>
            <li>Add <code className="bg-slate-900 px-2 py-1 rounded text-pcna-primary">TWILIO_AUTH_TOKEN</code> to backend/.env</li>
            <li>Add <code className="bg-slate-900 px-2 py-1 rounded text-pcna-primary">TWILIO_PHONE_NUMBER</code> to backend/.env</li>
            <li>Set <code className="bg-slate-900 px-2 py-1 rounded text-pcna-primary">SMS_MOCK_MODE=false</code></li>
            <li>Restart backend service</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default SMSConsole;
