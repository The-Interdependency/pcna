import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EDCMArtifacts = ({ backendUrl }) => {
  const [artifacts, setArtifacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedArtifact, setSelectedArtifact] = useState(null);

  useEffect(() => {
    fetchArtifacts();
  }, []);

  const fetchArtifacts = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${backendUrl}/api/edcm/artifacts`);
      setArtifacts(response.data.artifacts || []);
    } catch (error) {
      console.error('Error fetching artifacts:', error);
    }
    setLoading(false);
  };

  const generateNewArtifact = async () => {
    setLoading(true);
    try {
      await axios.get(`${backendUrl}/api/edcm/analyze`);
      await fetchArtifacts();
    } catch (error) {
      console.error('Error generating artifact:', error);
    }
    setLoading(false);
  };

  const getValueBadge = (value) => {
    const colors = {
      high: 'bg-green-500/20 text-green-400 border-green-500/30',
      medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      low: 'bg-blue-500/20 text-blue-400 border-blue-500/30'
    };
    return colors[value] || colors.low;
  };

  return (
    <div className="space-y-6" data-testid="edcm-artifacts">
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold">📈 EDCM Artifacts</h2>
            <p className="text-slate-400 mt-2">
              Entropy Dissonance Constraint Management reports for monetization
            </p>
          </div>
          <button
            onClick={generateNewArtifact}
            disabled={loading}
            className="px-6 py-3 bg-gradient-to-r from-pcna-primary to-pcna-secondary text-white rounded-lg hover:opacity-90 disabled:opacity-50 font-medium"
            data-testid="generate-artifact-btn"
          >
            {loading ? 'Generating...' : '✨ Generate New Artifact'}
          </button>
        </div>

        {/* Artifacts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {artifacts.map((artifact, idx) => (
            <div
              key={artifact._id || idx}
              onClick={() => setSelectedArtifact(artifact)}
              className="bg-slate-700/50 rounded-lg p-4 cursor-pointer hover:bg-slate-700 transition-all border border-slate-600 hover:border-pcna-primary"
            >
              <div className="flex justify-between items-start mb-3">
                <div className="text-sm text-slate-400">
                  {new Date(artifact.timestamp).toLocaleDateString()}
                </div>
                <span className={`px-2 py-1 rounded text-xs font-bold border ${getValueBadge(artifact.monetization_value)}`}>
                  {artifact.monetization_value?.toUpperCase()}
                </span>
              </div>

              <div className="space-y-2">
                <div>
                  <div className="text-xs text-slate-500">Entropy</div>
                  <div className="font-medium">
                    {artifact.analysis?.metrics?.entropy?.interpretation || 'N/A'}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-slate-500">Dissonance</div>
                  <div className="font-medium">
                    {artifact.analysis?.metrics?.dissonance?.interpretation || 'N/A'}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-slate-500">Insights</div>
                  <div className="font-medium">
                    {artifact.analysis?.insights?.length || 0} findings
                  </div>
                </div>
              </div>

              <div className="mt-3 text-xs text-pcna-primary">
                Click to view details →
              </div>
            </div>
          ))}
        </div>

        {artifacts.length === 0 && !loading && (
          <div className="text-center py-12 text-slate-500">
            <div className="text-4xl mb-4">📄</div>
            <p>No artifacts yet. Generate your first EDCM report!</p>
          </div>
        )}
      </div>

      {/* Artifact Details Modal */}
      {selectedArtifact && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-slate-700">
            <div className="sticky top-0 bg-slate-800 border-b border-slate-700 p-6 flex justify-between items-start">
              <div>
                <h3 className="text-2xl font-bold">EDCM Report Details</h3>
                <p className="text-slate-400 text-sm mt-1">
                  Generated: {new Date(selectedArtifact.timestamp).toLocaleString()}
                </p>
              </div>
              <button
                onClick={() => setSelectedArtifact(null)}
                className="text-slate-400 hover:text-white text-2xl"
              >
                ✕
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* Metrics */}
              <div>
                <h4 className="text-lg font-bold mb-4">Metrics</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-slate-700/50 rounded-lg p-4">
                    <div className="text-slate-400 text-sm mb-1">Entropy</div>
                    <div className="text-2xl font-bold text-pcna-primary">
                      {selectedArtifact.analysis?.metrics?.entropy?.interpretation || 'N/A'}
                    </div>
                    <div className="text-xs text-slate-500 mt-2">
                      Score: {selectedArtifact.analysis?.metrics?.entropy?.total_entropy?.toFixed(4)}
                    </div>
                  </div>
                  <div className="bg-slate-700/50 rounded-lg p-4">
                    <div className="text-slate-400 text-sm mb-1">Dissonance</div>
                    <div className="text-2xl font-bold text-pcna-secondary">
                      {selectedArtifact.analysis?.metrics?.dissonance?.interpretation || 'N/A'}
                    </div>
                    <div className="text-xs text-slate-500 mt-2">
                      Score: {selectedArtifact.analysis?.metrics?.dissonance?.dissonance_score?.toFixed(4)}
                    </div>
                  </div>
                  <div className="bg-slate-700/50 rounded-lg p-4">
                    <div className="text-slate-400 text-sm mb-1">Conservation Strain</div>
                    <div className="text-2xl font-bold text-pcna-accent">
                      {selectedArtifact.analysis?.metrics?.constraints?.strain_level || 'N/A'}
                    </div>
                    <div className="text-xs text-slate-500 mt-2">
                      {(selectedArtifact.analysis?.metrics?.constraints?.conservation_strain * 100)?.toFixed(2)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Insights */}
              <div>
                <h4 className="text-lg font-bold mb-3">Insights</h4>
                <div className="space-y-2">
                  {selectedArtifact.analysis?.insights?.map((insight, idx) => (
                    <div key={idx} className="bg-slate-700/50 rounded-lg p-3 flex items-start space-x-3">
                      <span className="text-pcna-primary text-xl">•</span>
                      <p className="flex-1">{insight}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              {selectedArtifact.analysis?.recommendations?.length > 0 && (
                <div>
                  <h4 className="text-lg font-bold mb-3">Recommendations</h4>
                  <div className="space-y-3">
                    {selectedArtifact.analysis.recommendations.map((rec, idx) => (
                      <div key={idx} className="bg-slate-700/50 rounded-lg p-4">
                        <div className="flex items-start space-x-3">
                          <span className={`px-2 py-1 rounded text-xs font-bold ${
                            rec.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                            rec.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-blue-500/20 text-blue-400'
                          }`}>
                            {rec.priority?.toUpperCase()}
                          </span>
                          <div className="flex-1">
                            <p className="font-medium mb-1">{rec.action}</p>
                            <p className="text-sm text-slate-400">{rec.reason}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Monetization Value */}
              <div className="bg-gradient-to-r from-pcna-primary/10 to-pcna-secondary/10 border border-pcna-primary/30 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-slate-400 text-sm">Monetization Value</div>
                    <div className="text-2xl font-bold mt-1">
                      {selectedArtifact.monetization_value?.toUpperCase()}
                    </div>
                  </div>
                  <div className="text-4xl">
                    {selectedArtifact.monetization_value === 'high' ? '💰' :
                     selectedArtifact.monetization_value === 'medium' ? '💵' : '💳'}
                  </div>
                </div>
                <p className="text-sm text-slate-400 mt-2">
                  This artifact contains {selectedArtifact.analysis?.insights?.length || 0} insights and {' '}
                  {selectedArtifact.analysis?.recommendations?.length || 0} actionable recommendations.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EDCMArtifacts;
