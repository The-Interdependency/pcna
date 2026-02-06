import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const SystemHealthDashboard = ({ systemState, backendUrl }) => {
  const [healthHistory, setHealthHistory] = useState([]);
  const [edcmAnalysis, setEdcmAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (systemState?.system_health) {
      setHealthHistory(prev => {
        const newHistory = [...prev, {
          timestamp: new Date().toLocaleTimeString(),
          health: systemState.system_health.average_health * 100,
          seeds: systemState.system_health.total_seeds
        }];
        return newHistory.slice(-20); // Keep last 20 data points
      });
    }
  }, [systemState]);

  const runEDCMAnalysis = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${backendUrl}/api/edcm/analyze`);
      setEdcmAnalysis(response.data);
    } catch (error) {
      console.error('EDCM analysis error:', error);
    }
    setLoading(false);
  };

  const seedsByRole = systemState ? Object.values(systemState.seeds || {}).reduce((acc, seed) => {
    acc[seed.role] = (acc[seed.role] || 0) + 1;
    return acc;
  }, {}) : {};

  const healthStatus = systemState?.system_health?.status || 'UNKNOWN';
  const avgHealth = systemState?.system_health?.average_health || 0;

  return (
    <div className="space-y-6" data-testid="system-health-dashboard">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">System Status</p>
              <p className={`text-2xl font-bold mt-2 ${
                healthStatus === 'HEALTHY' ? 'text-green-400' :
                healthStatus === 'DEGRADED' ? 'text-yellow-400' :
                'text-red-400'
              }`}>
                {healthStatus}
              </p>
            </div>
            <div className="text-4xl">
              {healthStatus === 'HEALTHY' ? '✅' : healthStatus === 'DEGRADED' ? '⚠️' : '🔴'}
            </div>
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Average Health</p>
              <p className="text-2xl font-bold mt-2 text-pcna-primary">
                {(avgHealth * 100).toFixed(1)}%
              </p>
            </div>
            <div className="text-4xl">💚</div>
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Active Seeds</p>
              <p className="text-2xl font-bold mt-2 text-pcna-secondary">
                {systemState?.system_health?.total_seeds || 0}
              </p>
            </div>
            <div className="text-4xl">🌱</div>
          </div>
        </div>

        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Compute Seeds</p>
              <p className="text-2xl font-bold mt-2 text-pcna-accent">
                {seedsByRole.compute || 0}
              </p>
            </div>
            <div className="text-4xl">⚙️</div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Health Trend */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <h3 className="text-xl font-bold mb-4">Health Trend</h3>
          {healthHistory.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={healthHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="timestamp" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" domain={[0, 100]} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} />
                <Legend />
                <Line type="monotone" dataKey="health" stroke="#6366f1" strokeWidth={2} name="Health %" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-slate-500">
              Waiting for data...
            </div>
          )}
        </div>

        {/* Seed Distribution */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <h3 className="text-xl font-bold mb-4">Seed Distribution by Role</h3>
          <div className="space-y-4">
            {Object.entries(seedsByRole).map(([role, count]) => (
              <div key={role}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400 capitalize">{role}</span>
                  <span className="text-white font-bold">{count}</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-pcna-primary to-pcna-secondary h-2 rounded-full transition-all"
                    style={{ width: `${(count / (systemState?.system_health?.total_seeds || 1)) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* EDCM Analysis */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">EDCM Analysis</h3>
          <button
            onClick={runEDCMAnalysis}
            disabled={loading}
            className="px-4 py-2 bg-gradient-to-r from-pcna-primary to-pcna-secondary text-white rounded-lg hover:opacity-90 disabled:opacity-50"
            data-testid="run-edcm-analysis-btn"
          >
            {loading ? 'Analyzing...' : 'Run Analysis'}
          </button>
        </div>

        {edcmAnalysis ? (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-700/50 rounded-lg p-4">
                <p className="text-slate-400 text-sm">Entropy</p>
                <p className="text-xl font-bold text-pcna-primary mt-1">
                  {edcmAnalysis.metrics?.entropy?.interpretation || 'N/A'}
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  Score: {edcmAnalysis.metrics?.entropy?.total_entropy?.toFixed(3)}
                </p>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-4">
                <p className="text-slate-400 text-sm">Dissonance</p>
                <p className="text-xl font-bold text-pcna-secondary mt-1">
                  {edcmAnalysis.metrics?.dissonance?.interpretation || 'N/A'}
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  Score: {edcmAnalysis.metrics?.dissonance?.dissonance_score?.toFixed(3)}
                </p>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-4">
                <p className="text-slate-400 text-sm">Conservation Strain</p>
                <p className="text-xl font-bold text-pcna-accent mt-1">
                  {edcmAnalysis.metrics?.constraints?.strain_level || 'N/A'}
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  Strain: {(edcmAnalysis.metrics?.constraints?.conservation_strain * 100)?.toFixed(2)}%
                </p>
              </div>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-2">Insights</h4>
              <ul className="space-y-2">
                {edcmAnalysis.insights?.map((insight, idx) => (
                  <li key={idx} className="flex items-start space-x-2 text-slate-300">
                    <span className="text-pcna-primary mt-1">•</span>
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            </div>

            {edcmAnalysis.recommendations?.length > 0 && (
              <div>
                <h4 className="text-lg font-semibold mb-2">Recommendations</h4>
                <div className="space-y-2">
                  {edcmAnalysis.recommendations.map((rec, idx) => (
                    <div key={idx} className="bg-slate-700/50 rounded-lg p-3 flex items-start space-x-3">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${
                        rec.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                        rec.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {rec.priority.toUpperCase()}
                      </span>
                      <div>
                        <p className="font-medium">{rec.action}</p>
                        <p className="text-sm text-slate-400">{rec.reason}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-12 text-slate-500">
            Click "Run Analysis" to generate EDCM metrics and insights
          </div>
        )}
      </div>
    </div>
  );
};

export default SystemHealthDashboard;
