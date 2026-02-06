"""
Self-Optimization Engine for PCNA
Monitors system health and automatically adjusts resources
"""
import logging
from typing import Dict, List, Any
from datetime import datetime
import numpy as np

logger = logging.getLogger("self_optimizer")

class SelfOptimizer:
    """
    Monitors PCNA system and automatically optimizes:
    - Seed allocation based on load
    - Health degradation detection
    - Resource reallocation
    - Anomaly detection
    """
    def __init__(self, topology):
        self.topology = topology
        self.health_history = []
        self.optimization_history = []
        self.health_threshold_degraded = 0.7
        self.health_threshold_critical = 0.4
        
    async def optimize(self, active_seeds: Dict) -> Dict[str, Any]:
        """
        Run optimization cycle
        
        Returns:
            Dict with optimization results and actions taken
        """
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "actions_taken": [],
            "recommendations": [],
            "health_summary": {}
        }
        
        # 1. Calculate system health
        health_metrics = self._calculate_health(active_seeds)
        result["health_summary"] = health_metrics
        self.health_history.append(health_metrics)
        
        # 2. Detect anomalies
        anomalies = self._detect_anomalies(active_seeds)
        if anomalies:
            result["actions_taken"].append(f"Detected {len(anomalies)} anomalies")
            logger.warning(f"Anomalies detected: {anomalies}")
        
        # 3. Check for degraded seeds
        degraded_seeds = [
            sid for sid, seed in active_seeds.items() 
            if seed.health_score < self.health_threshold_degraded
        ]
        
        if degraded_seeds:
            result["actions_taken"].append(f"Flagged {len(degraded_seeds)} degraded seeds")
            result["recommendations"].append({
                "action": "restart_seeds",
                "seed_ids": degraded_seeds,
                "reason": "health below threshold"
            })
        
        # 4. Check mass conservation
        conservation_violations = self._check_conservation(active_seeds)
        if conservation_violations:
            result["actions_taken"].append(f"Mass conservation violations: {conservation_violations}")
            logger.error(f"Conservation violations: {conservation_violations}")
        
        # 5. Optimize load balancing
        if health_metrics["average_health"] < self.health_threshold_critical:
            result["actions_taken"].append("System critical - triggering emergency rebalance")
            result["recommendations"].append({
                "action": "emergency_rebalance",
                "reason": "system health critical"
            })
        
        # Store optimization result
        self.optimization_history.append(result)
        
        return result
    
    def _calculate_health(self, active_seeds: Dict) -> Dict[str, Any]:
        """Calculate overall system health metrics"""
        if not active_seeds:
            return {
                "average_health": 0.0,
                "min_health": 0.0,
                "max_health": 0.0,
                "total_seeds": 0
            }
        
        health_scores = [seed.health_score for seed in active_seeds.values()]
        
        return {
            "average_health": np.mean(health_scores),
            "min_health": np.min(health_scores),
            "max_health": np.max(health_scores),
            "std_dev": np.std(health_scores),
            "total_seeds": len(active_seeds)
        }
    
    def _detect_anomalies(self, active_seeds: Dict) -> List[Dict[str, Any]]:
        """Detect anomalous seed behavior"""
        anomalies = []
        
        # Check for seeds with extreme spectral descriptors
        for sid, seed in active_seeds.items():
            if seed.state:
                magnitude, phase = seed.state.spectral_descriptor()
                
                # Check for extreme values
                if magnitude > 100 or magnitude < 0.001:
                    anomalies.append({
                        "seed_id": sid,
                        "type": "spectral_magnitude",
                        "value": magnitude,
                        "severity": "high" if magnitude > 100 else "medium"
                    })
                
                # Check mass
                if seed.state.mass < 0.1 or seed.state.mass > 10:
                    anomalies.append({
                        "seed_id": sid,
                        "type": "mass_outlier",
                        "value": seed.state.mass,
                        "severity": "high"
                    })
        
        return anomalies
    
    def _check_conservation(self, active_seeds: Dict) -> List[str]:
        """Check mass conservation across system"""
        violations = []
        
        # Calculate total system mass
        total_mass = sum(
            seed.state.mass for seed in active_seeds.values() 
            if seed.state is not None
        )
        
        # Expected mass (assuming each compute seed starts with 1.0)
        compute_seeds = [s for s in active_seeds.values() if s.role.value == "compute"]
        expected_mass = len(compute_seeds) * 1.0
        
        # Check conservation (allow 1% tolerance)
        if abs(total_mass - expected_mass) > expected_mass * 0.01:
            violations.append(
                f"Total mass {total_mass:.4f} deviates from expected {expected_mass:.4f}"
            )
        
        return violations
    
    def get_health_trend(self, window: int = 10) -> Dict[str, Any]:
        """Get health trend over recent history"""
        if len(self.health_history) < 2:
            return {"trend": "insufficient_data"}
        
        recent = self.health_history[-window:]
        health_values = [h["average_health"] for h in recent]
        
        # Simple linear trend
        if len(health_values) >= 2:
            trend = (health_values[-1] - health_values[0]) / len(health_values)
            
            return {
                "trend": "improving" if trend > 0.01 else "degrading" if trend < -0.01 else "stable",
                "slope": trend,
                "current_health": health_values[-1],
                "window_size": len(health_values)
            }
        
        return {"trend": "stable"}
