"""
EDCM (Entropy Dissonance Constraint Management) Analyzer
Generates artifacts for monetization and system diagnostics
"""
import logging
from typing import Dict, List, Any
from datetime import datetime
import numpy as np

logger = logging.getLogger("edcm_analyzer")

class EDCMAnalyzer:
    """
    Analyzes PCNA system using EDCM principles:
    - Entropy measurement
    - Dissonance detection
    - Constraint strain analysis
    - Generates monetizable artifacts (reports, visualizations, insights)
    """
    def __init__(self):
        self.analysis_history = []
        
    async def analyze(self, seed_states: List[Dict]) -> Dict[str, Any]:
        """
        Perform EDCM analysis on system state
        
        Args:
            seed_states: List of seed state dictionaries
            
        Returns:
            EDCM analysis report (monetizable artifact)
        """
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "artifact_type": "edcm_report",
            "version": "1.0",
            "metrics": {},
            "insights": [],
            "recommendations": [],
            "monetization_value": "medium"  # low, medium, high
        }
        
        # 1. Calculate Entropy
        entropy_metrics = self._calculate_entropy(seed_states)
        analysis["metrics"]["entropy"] = entropy_metrics
        
        # 2. Detect Dissonance
        dissonance_metrics = self._detect_dissonance(seed_states)
        analysis["metrics"]["dissonance"] = dissonance_metrics
        
        # 3. Analyze Constraint Strain
        constraint_metrics = self._analyze_constraints(seed_states)
        analysis["metrics"]["constraints"] = constraint_metrics
        
        # 4. Generate Insights
        insights = self._generate_insights(entropy_metrics, dissonance_metrics, constraint_metrics)
        analysis["insights"] = insights
        
        # 5. Generate Recommendations
        recommendations = self._generate_recommendations(analysis["metrics"])
        analysis["recommendations"] = recommendations
        
        # 6. Assess artifact value for monetization
        analysis["monetization_value"] = self._assess_artifact_value(analysis)
        
        # Store in history
        self.analysis_history.append(analysis)
        
        logger.info(f"EDCM analysis complete: {len(insights)} insights, {len(recommendations)} recommendations")
        
        return analysis
    
    def _calculate_entropy(self, seed_states: List[Dict]) -> Dict[str, Any]:
        """Calculate system entropy"""
        if not seed_states:
            return {"total_entropy": 0.0, "average_entropy": 0.0}
        
        # Calculate spectral entropy from seed phases
        phases = []
        for state in seed_states:
            if state.get("spectral"):
                phases.append(state["spectral"].get("phase", 0.0))
        
        if not phases:
            return {"total_entropy": 0.0, "average_entropy": 0.0}
        
        # Shannon entropy approximation
        phase_array = np.array(phases)
        # Normalize phases to [0, 1]
        normalized_phases = (phase_array + np.pi) / (2 * np.pi)
        
        # Calculate entropy
        hist, _ = np.histogram(normalized_phases, bins=10)
        hist = hist / hist.sum()  # Normalize to probabilities
        entropy = -np.sum(hist * np.log2(hist + 1e-10))  # Shannon entropy
        
        return {
            "total_entropy": float(entropy),
            "average_entropy": float(entropy / len(phases)),
            "phase_distribution": hist.tolist(),
            "interpretation": "high" if entropy > 2.5 else "medium" if entropy > 1.5 else "low"
        }
    
    def _detect_dissonance(self, seed_states: List[Dict]) -> Dict[str, Any]:
        """Detect dissonance in system"""
        if not seed_states:
            return {"dissonance_score": 0.0, "dissonant_seeds": []}
        
        # Dissonance = deviation from expected patterns
        health_scores = [s["health_score"] for s in seed_states]
        
        # Calculate variance as dissonance measure
        variance = np.var(health_scores)
        dissonance_score = float(variance * 10)  # Scale for readability
        
        # Identify dissonant seeds (outliers)
        mean_health = np.mean(health_scores)
        std_health = np.std(health_scores)
        
        dissonant_seeds = []
        for state in seed_states:
            if abs(state["health_score"] - mean_health) > 2 * std_health:
                dissonant_seeds.append({
                    "seed_id": state["seed_id"],
                    "health_score": state["health_score"],
                    "deviation": abs(state["health_score"] - mean_health)
                })
        
        return {
            "dissonance_score": dissonance_score,
            "dissonant_seeds": dissonant_seeds,
            "health_variance": float(variance),
            "interpretation": "high" if dissonance_score > 1.0 else "medium" if dissonance_score > 0.5 else "low"
        }
    
    def _analyze_constraints(self, seed_states: List[Dict]) -> Dict[str, Any]:
        """Analyze constraint strain"""
        # Calculate mass conservation constraint
        total_mass = sum(s["mass"] for s in seed_states)
        expected_mass = sum(1.0 for s in seed_states if s.get("role") == "compute")
        
        conservation_strain = abs(total_mass - expected_mass) / (expected_mass + 1e-10)
        
        return {
            "total_mass": float(total_mass),
            "expected_mass": float(expected_mass),
            "conservation_strain": float(conservation_strain),
            "strain_level": "critical" if conservation_strain > 0.1 else "warning" if conservation_strain > 0.01 else "normal"
        }
    
    def _generate_insights(self, 
                          entropy_metrics: Dict, 
                          dissonance_metrics: Dict, 
                          constraint_metrics: Dict) -> List[str]:
        """Generate human-readable insights"""
        insights = []
        
        # Entropy insights
        if entropy_metrics["interpretation"] == "high":
            insights.append("System exhibits high entropy - indicates diverse, distributed processing")
        elif entropy_metrics["interpretation"] == "low":
            insights.append("Low entropy detected - system may be overly synchronized")
        
        # Dissonance insights
        if dissonance_metrics["dissonant_seeds"]:
            insights.append(f"{len(dissonance_metrics['dissonant_seeds'])} seeds showing dissonance - potential optimization targets")
        
        # Constraint insights
        if constraint_metrics["strain_level"] != "normal":
            insights.append(f"Mass conservation strain at {constraint_metrics['strain_level']} level")
        
        # Overall system health insight
        if not insights:
            insights.append("System operating within normal EDCM parameters")
        
        return insights
    
    def _generate_recommendations(self, metrics: Dict) -> List[Dict[str, str]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Entropy-based recommendations
        entropy = metrics["entropy"]["interpretation"]
        if entropy == "high":
            recommendations.append({
                "priority": "low",
                "action": "Monitor entropy trends",
                "reason": "High entropy may indicate inefficiency if sustained"
            })
        
        # Dissonance-based recommendations
        if metrics["dissonance"]["dissonant_seeds"]:
            recommendations.append({
                "priority": "medium",
                "action": "Investigate dissonant seeds",
                "reason": f"{len(metrics['dissonance']['dissonant_seeds'])} seeds showing outlier behavior"
            })
        
        # Constraint-based recommendations
        strain_level = metrics["constraints"]["strain_level"]
        if strain_level == "critical":
            recommendations.append({
                "priority": "high",
                "action": "Emergency system rebalance",
                "reason": "Mass conservation critically violated"
            })
        elif strain_level == "warning":
            recommendations.append({
                "priority": "medium",
                "action": "Schedule system tune-up",
                "reason": "Mass conservation showing strain"
            })
        
        return recommendations
    
    def _assess_artifact_value(self, analysis: Dict) -> str:
        """Assess monetization value of artifact"""
        # High value if:
        # - Critical issues detected
        # - Multiple actionable recommendations
        # - Novel insights
        
        recommendations = analysis["recommendations"]
        high_priority = sum(1 for r in recommendations if r["priority"] == "high")
        insights_count = len(analysis["insights"])
        
        if high_priority > 0 or insights_count > 3:
            return "high"
        elif len(recommendations) > 1:
            return "medium"
        else:
            return "low"
    
    def get_artifact_summary(self, limit: int = 5) -> Dict[str, Any]:
        """Get summary of recent artifacts for monetization dashboard"""
        recent = self.analysis_history[-limit:]
        
        return {
            "total_artifacts": len(self.analysis_history),
            "recent_artifacts": recent,
            "value_distribution": {
                "high": sum(1 for a in recent if a["monetization_value"] == "high"),
                "medium": sum(1 for a in recent if a["monetization_value"] == "medium"),
                "low": sum(1 for a in recent if a["monetization_value"] == "low")
            }
        }
