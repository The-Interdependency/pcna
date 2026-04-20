"""
EDCM (Entropy Dissonance Constraint Management) Analyzer

Six metric families (from a0 canonical spec):
  CM      — Constraint Mismatch        alert: HIGH >= 0.80
  DA      — Dissonance Accumulation    alert: HIGH >= 0.80
  DRIFT   — Drift                      alert: HIGH >= 0.80
  DVG     — Divergence                 alert: HIGH >= 0.80
  INT     — Intensity                  alert: LOW  <= 0.20
  TBF     — Turn-Balance Fairness      alert: LOW  <= 0.20

EDCM Behavioral Directives (fire when metric crosses threshold):
  CONSTRAINT_REFOCUS  — CM   >= 0.80
  DISSONANCE_HALT     — DA   >= 0.80
  DRIFT_ANCHOR        — DRIFT>= 0.80
  DIVERGENCE_COMMIT   — DVG  >= 0.80
  INTENSITY_CALM      — INT  <= 0.20
  BALANCE_CONCISE     — TBF  <= 0.20
"""
import math
import logging
from typing import Dict, List, Any
from datetime import datetime

from core.edcm import (
    METRIC_NAMES,
    ALERT_HIGH,
    ALERT_LOW,
    check_alerts,
)

logger = logging.getLogger("edcm_analyzer")


class EDCMAnalyzer:
    """
    Analyzes PCNA system state using the six-family EDCM metric framework.
    Generates diagnostic artifacts and fires behavioral directives when
    metrics cross thresholds.
    """

    def __init__(self):
        self.analysis_history: List[Dict] = []

    async def analyze(self, seed_states: List[Dict]) -> Dict[str, Any]:
        """
        Perform six-family EDCM analysis on system state.

        Args:
            seed_states: list of seed state dicts (must include 'health_score' and 'mass').

        Returns:
            EDCM analysis report with metrics, alerts, directives, insights, recommendations.
        """
        analysis: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "artifact_type": "edcm_report",
            "version": "2.0",
            "metrics": {},
            "alerts": {},
            "directives": [],
            "insights": [],
            "recommendations": [],
            "monetization_value": "medium",
        }

        metrics = self._compute_from_seeds(seed_states)
        analysis["metrics"] = metrics

        alerts = check_alerts(metrics)
        analysis["alerts"] = alerts

        directives = self._fire_directives(metrics)
        analysis["directives"] = directives

        insights = self._generate_insights(metrics, alerts, directives)
        analysis["insights"] = insights

        recommendations = self._generate_recommendations(metrics, alerts)
        analysis["recommendations"] = recommendations

        analysis["monetization_value"] = self._assess_artifact_value(analysis)

        self.analysis_history.append(analysis)

        logger.info(
            f"EDCM analysis: metrics={metrics} alerts={alerts} "
            f"directives={directives} insights={len(insights)}"
        )

        return analysis

    def _compute_from_seeds(self, seed_states: List[Dict]) -> Dict[str, float]:
        """Derive six EDCM metrics from seed state list."""
        if not seed_states:
            return {m: 0.0 for m in METRIC_NAMES}

        health_scores = [s.get("health_score", 0.0) for s in seed_states]
        masses = [s.get("mass", 0.0) for s in seed_states]

        n = len(health_scores)
        mean_h = sum(health_scores) / max(n, 1)
        variance_h = sum((h - mean_h) ** 2 for h in health_scores) / max(n, 1)

        # CM: mass conservation deviation — how far total mass deviates from expected
        compute_seeds = [s for s in seed_states if s.get("role") == "compute"]
        expected_mass = len(compute_seeds) if compute_seeds else n
        total_mass = sum(masses)
        cm = min(1.0, abs(total_mass - expected_mass) / max(expected_mass, 1))

        # DA: dissonance accumulation — normalized health variance
        da = min(1.0, math.sqrt(variance_h))

        # DRIFT: deviation from healthy baseline (1.0)
        drift = max(0.0, min(1.0, 1.0 - mean_h))

        # DVG: fraction of outlier seeds (> 2 std from mean)
        std_h = math.sqrt(variance_h)
        outliers = sum(1 for h in health_scores if abs(h - mean_h) > 2 * std_h)
        dvg = min(1.0, outliers / max(n, 1))

        # INT: system intensity — mean health as proxy for active processing
        int_val = max(0.0, min(1.0, mean_h))

        # TBF: turn-balance fairness — inverse of health std (balanced = fair)
        tbf = max(0.0, min(1.0, 1.0 - std_h))

        return {
            "cm": round(cm, 4),
            "da": round(da, 4),
            "drift": round(drift, 4),
            "dvg": round(dvg, 4),
            "int_val": round(int_val, 4),
            "tbf": round(tbf, 4),
        }

    def _fire_directives(self, metrics: Dict[str, float]) -> List[str]:
        """Map metric threshold crossings to EDCM behavioral directives."""
        fired = []
        if metrics.get("cm", 0.0) >= ALERT_HIGH:
            fired.append("CONSTRAINT_REFOCUS")
        if metrics.get("da", 0.0) >= ALERT_HIGH:
            fired.append("DISSONANCE_HALT")
        if metrics.get("drift", 0.0) >= ALERT_HIGH:
            fired.append("DRIFT_ANCHOR")
        if metrics.get("dvg", 0.0) >= ALERT_HIGH:
            fired.append("DIVERGENCE_COMMIT")
        if metrics.get("int_val", 0.0) <= ALERT_LOW:
            fired.append("INTENSITY_CALM")
        if metrics.get("tbf", 0.0) <= ALERT_LOW:
            fired.append("BALANCE_CONCISE")
        return fired

    def _generate_insights(
        self,
        metrics: Dict[str, float],
        alerts: Dict[str, List[str]],
        directives: List[str],
    ) -> List[str]:
        insights = []
        high = alerts.get("HIGH", [])
        low = alerts.get("LOW", [])

        if "cm" in high:
            insights.append("HIGH CM: mass conservation violated — system energy imbalance detected")
        if "da" in high:
            insights.append("HIGH DA: dissonance accumulation elevated — seed health diverging")
        if "drift" in high:
            insights.append("HIGH DRIFT: system drifting from healthy baseline")
        if "dvg" in high:
            insights.append("HIGH DVG: divergence elevated — significant outlier seeds present")
        if "int_val" in low:
            insights.append("LOW INT: system intensity suppressed — reduced active processing")
        if "tbf" in low:
            insights.append("LOW TBF: turn-balance fairness degraded — uneven load distribution")

        for directive in directives:
            insights.append(f"Directive fired: {directive}")

        if not insights:
            insights.append("System operating within normal EDCM parameters")

        return insights

    def _generate_recommendations(
        self, metrics: Dict[str, float], alerts: Dict[str, List[str]]
    ) -> List[Dict[str, str]]:
        recommendations = []
        high = alerts.get("HIGH", [])
        low = alerts.get("LOW", [])

        if "cm" in high:
            recommendations.append({
                "priority": "high",
                "action": "Emergency system rebalance",
                "reason": "Mass conservation critically violated (CM >= 0.80)",
            })
        if "da" in high:
            recommendations.append({
                "priority": "high",
                "action": "Investigate dissonant seeds",
                "reason": "Dissonance accumulation above threshold (DA >= 0.80)",
            })
        if "drift" in high:
            recommendations.append({
                "priority": "medium",
                "action": "Re-anchor system to healthy baseline",
                "reason": "Drift exceeds safe operating range (DRIFT >= 0.80)",
            })
        if "dvg" in high:
            recommendations.append({
                "priority": "medium",
                "action": "Quarantine or rebalance outlier seeds",
                "reason": "Divergence elevated — outlier seeds detected (DVG >= 0.80)",
            })
        if "int_val" in low:
            recommendations.append({
                "priority": "medium",
                "action": "Boost system intensity",
                "reason": "Intensity suppressed below safe floor (INT <= 0.20)",
            })
        if "tbf" in low:
            recommendations.append({
                "priority": "low",
                "action": "Redistribute load across seeds",
                "reason": "Turn-balance fairness degraded (TBF <= 0.20)",
            })

        return recommendations

    def _assess_artifact_value(self, analysis: Dict) -> str:
        high_recs = sum(1 for r in analysis["recommendations"] if r["priority"] == "high")
        if high_recs > 0 or len(analysis["directives"]) > 0:
            return "high"
        elif len(analysis["recommendations"]) > 1:
            return "medium"
        return "low"

    def get_artifact_summary(self, limit: int = 5) -> Dict[str, Any]:
        recent = self.analysis_history[-limit:]
        return {
            "total_artifacts": len(self.analysis_history),
            "recent_artifacts": recent,
            "value_distribution": {
                "high": sum(1 for a in recent if a["monetization_value"] == "high"),
                "medium": sum(1 for a in recent if a["monetization_value"] == "medium"),
                "low": sum(1 for a in recent if a["monetization_value"] == "low"),
            },
        }
