import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TopologyVisualization = ({ systemState, backendUrl }) => {
  const [topology, setTopology] = useState(null);
  const [selectedSeed, setSelectedSeed] = useState(null);

  useEffect(() => {
    fetchTopology();
  }, []);

  const fetchTopology = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/topology`);
      setTopology(response.data);
    } catch (error) {
      console.error('Error fetching topology:', error);
    }
  };

  const getSeedColor = (role) => {
    switch (role) {
      case 'global': return '#ec4899';
      case 'sentinel': return '#f59e0b';
      case 'meta': return '#8b5cf6';
      case 'compute': return '#6366f1';
      default: return '#64748b';
    }
  };

  const getRoleIcon = (role) => {
    switch (role) {
      case 'global': return '🌐';
      case 'sentinel': return '🕶';
      case 'meta': return '🧠';
      case 'compute': return '⚙️';
      default: return '●';
    }
  };

  const currentSeeds = systemState?.seeds || {};

  return (
    <div className="space-y-6" data-testid="topology-visualization">
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <h2 className="text-2xl font-bold mb-4">PCNA Topology Map</h2>
        <p className="text-slate-400 mb-6">
          Prime Circular Neural Architecture - 53 seed network with heptagram routing
        </p>

        {/* Legend */}
        <div className="flex flex-wrap gap-4 mb-6">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full" style={{ backgroundColor: getSeedColor('global') }}></div>
            <span className="text-sm">Global Router (1)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full" style={{ backgroundColor: getSeedColor('sentinel') }}></div>
            <span className="text-sm">Sentinels (4)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full" style={{ backgroundColor: getSeedColor('meta') }}></div>
            <span className="text-sm">Meta Routers (7)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded-full" style={{ backgroundColor: getSeedColor('compute') }}></div>
            <span className="text-sm">Compute Seeds (49)</span>
          </div>
        </div>

        {/* Circular Visualization */}
        <div className="relative w-full h-96 bg-slate-900/50 rounded-lg flex items-center justify-center">
          <svg width="100%" height="100%" viewBox="0 0 400 400">
            {/* Draw connections (heptagram pattern) */}
            {topology && Object.entries(topology).map(([id, seed]) => {
              if (seed.neighbors && seed.neighbors.length > 0) {
                const angle1 = (parseInt(id) / 53) * 2 * Math.PI;
                const x1 = 200 + Math.cos(angle1) * 150;
                const y1 = 200 + Math.sin(angle1) * 150;

                return seed.neighbors.map((neighborId, idx) => {
                  const angle2 = (neighborId / 53) * 2 * Math.PI;
                  const x2 = 200 + Math.cos(angle2) * 150;
                  const y2 = 200 + Math.sin(angle2) * 150;

                  return (
                    <line
                      key={`${id}-${neighborId}-${idx}`}
                      x1={x1}
                      y1={y1}
                      x2={x2}
                      y2={y2}
                      stroke="#475569"
                      strokeWidth="0.5"
                      opacity="0.3"
                    />
                  );
                });
              }
              return null;
            })}

            {/* Draw nodes */}
            {topology && Object.entries(topology).map(([id, seed]) => {
              const angle = (parseInt(id) / 53) * 2 * Math.PI;
              const radius = seed.role === 'global' ? 0 : 
                            seed.role === 'sentinel' ? 100 :
                            seed.role === 'meta' ? 130 : 150;
              const x = 200 + Math.cos(angle) * radius;
              const y = 200 + Math.sin(angle) * radius;

              const currentSeed = currentSeeds[id];
              const isActive = currentSeed !== undefined;
              const health = currentSeed?.health_score || 0;

              return (
                <g
                  key={id}
                  onClick={() => setSelectedSeed({ ...seed, ...currentSeed })}
                  style={{ cursor: 'pointer' }}
                >
                  <circle
                    cx={x}
                    cy={y}
                    r={seed.role === 'global' ? 8 : 5}
                    fill={getSeedColor(seed.role)}
                    opacity={isActive ? 0.9 : 0.3}
                    stroke={isActive && health < 0.7 ? '#ef4444' : '#ffffff'}
                    strokeWidth={isActive && health < 0.7 ? 2 : 0}
                  />
                  {seed.role === 'global' && (
                    <text x={x} y={y + 25} textAnchor="middle" fill="#f1f5f9" fontSize="12">
                      Global
                    </text>
                  )}
                </g>
              );
            })}
          </svg>
        </div>
      </div>

      {/* Seed Details */}
      {selectedSeed && (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
          <div className="flex justify-between items-start mb-4">
            <h3 className="text-xl font-bold flex items-center space-x-2">
              <span>{getRoleIcon(selectedSeed.role)}</span>
              <span>Seed #{selectedSeed.id} - {selectedSeed.role.toUpperCase()}</span>
            </h3>
            <button
              onClick={() => setSelectedSeed(null)}
              className="text-slate-400 hover:text-white"
            >
              ✕
            </button>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-slate-400 text-sm">Role</p>
              <p className="text-white font-medium">{selectedSeed.role}</p>
            </div>
            {selectedSeed.meta_id && (
              <div>
                <p className="text-slate-400 text-sm">Meta ID</p>
                <p className="text-white font-medium">{selectedSeed.meta_id}</p>
              </div>
            )}
            {selectedSeed.health_score !== undefined && (
              <div>
                <p className="text-slate-400 text-sm">Health Score</p>
                <p className={`text-xl font-bold ${
                  selectedSeed.health_score > 0.8 ? 'text-green-400' :
                  selectedSeed.health_score > 0.5 ? 'text-yellow-400' :
                  'text-red-400'
                }`}>
                  {(selectedSeed.health_score * 100).toFixed(1)}%
                </p>
              </div>
            )}
            {selectedSeed.tick !== undefined && (
              <div>
                <p className="text-slate-400 text-sm">Current Tick</p>
                <p className="text-white font-medium">{selectedSeed.tick}</p>
              </div>
            )}
            {selectedSeed.mass !== undefined && (
              <div>
                <p className="text-slate-400 text-sm">Mass</p>
                <p className="text-white font-medium">{selectedSeed.mass.toFixed(4)}</p>
              </div>
            )}
            {selectedSeed.spectral && (
              <>
                <div>
                  <p className="text-slate-400 text-sm">Spectral Magnitude</p>
                  <p className="text-white font-medium">{selectedSeed.spectral.magnitude.toFixed(4)}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Spectral Phase</p>
                  <p className="text-white font-medium">{selectedSeed.spectral.phase.toFixed(4)}</p>
                </div>
              </>
            )}
          </div>

          {selectedSeed.neighbors && selectedSeed.neighbors.length > 0 && (
            <div className="mt-4">
              <p className="text-slate-400 text-sm mb-2">Neighbors (7:3 Heptagram)</p>
              <div className="flex flex-wrap gap-2">
                {selectedSeed.neighbors.map((nId) => (
                  <span
                    key={nId}
                    className="px-3 py-1 bg-pcna-primary/20 text-pcna-primary rounded-full text-sm"
                  >
                    #{nId}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Active Seeds List */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 border border-slate-700">
        <h3 className="text-xl font-bold mb-4">Active Seeds</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {Object.entries(currentSeeds).map(([id, seed]) => (
            <div
              key={id}
              onClick={() => setSelectedSeed({ ...topology?.[id], ...seed })}
              className="bg-slate-700/50 rounded-lg p-4 cursor-pointer hover:bg-slate-700 transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span>{getRoleIcon(seed.role)}</span>
                  <span className="font-medium">Seed #{id}</span>
                </div>
                <div className={`w-3 h-3 rounded-full ${
                  seed.health_score > 0.8 ? 'bg-green-500' :
                  seed.health_score > 0.5 ? 'bg-yellow-500' :
                  'bg-red-500'
                }`}></div>
              </div>
              <div className="mt-2 text-sm text-slate-400">
                Health: {(seed.health_score * 100).toFixed(1)}% | Tick: {seed.tick}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TopologyVisualization;
