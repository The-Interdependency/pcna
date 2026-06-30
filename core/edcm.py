# ratios: loc_comments=65:33 imports_exports=2:4 calls_definitions=23:4
"""
EDCM metrics — six-family coherence measurement.

Metric families:
  cm      — Constraint Mismatch
  da      — Dissonance Accumulation
  drift   — Drift
  dvg     — Divergence
  int_val — Intensity
  tbf     — Turn-Balance Fairness

All metrics produce values in [0, 1].
Alert thresholds: HIGH >= 0.80, LOW <= 0.20.
"""

# === MODULE_BUILD ===
# id: pcna_edcm
#   module_name: edcm
#   module_kind: engine
#   summary: Six-family EDCM coherence metrics (cm, da, drift, dvg, int_val, tbf) computed from response text, with alert thresholds and corrective directive firing.
#   owner: Erin Spencer
#   public_surface: compute_metrics, check_directives, check_alerts, delta_between, METRIC_NAMES, ALERT_HIGH, ALERT_LOW, DIRECTIVES
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_edcm_engine.py
#   rollout: default_enabled
#   rollback: remove import and call sites
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

import math
from typing import Any

METRIC_NAMES = ["cm", "da", "drift", "dvg", "int_val", "tbf"]

ALERT_HIGH = 0.80
ALERT_LOW = 0.20

DIRECTIVES = {
    "CONSTRAINT_REFOCUS": {"metric": "cm", "condition": "above", "threshold": ALERT_HIGH},
    "DISSONANCE_HALT": {"metric": "da", "condition": "above", "threshold": ALERT_HIGH},
    "DRIFT_ANCHOR": {"metric": "drift", "condition": "above", "threshold": ALERT_HIGH},
    "DIVERGENCE_COMMIT": {"metric": "dvg", "condition": "above", "threshold": ALERT_HIGH},
    "INTENSITY_CALM": {"metric": "int_val", "condition": "below", "threshold": ALERT_LOW},
    "BALANCE_CONCISE": {"metric": "tbf", "condition": "below", "threshold": ALERT_LOW},
}


def compute_metrics(
    responses: list[dict[str, Any]],
    context: str = "",
) -> dict[str, float]:
    if not responses:
        return {m: 0.0 for m in METRIC_NAMES}
    n = len(responses)
    texts = [r.get("content", "") for r in responses]
    avg_len = sum(len(t) for t in texts) / max(n, 1)
    variance = sum((len(t) - avg_len) ** 2 for t in texts) / max(n, 1)
    std = math.sqrt(variance)

    cm = min(1.0, avg_len / 2000) if avg_len > 0 else 0.0
    da = max(0.0, 1.0 - std / max(avg_len, 1))
    drift = min(1.0, std / max(avg_len, 1))
    unique_starts = len(set(t[:50] for t in texts if t))
    dvg = min(1.0, unique_starts / max(n, 1))
    int_val = max(0.0, 1.0 - drift * 0.5 - dvg * 0.3)
    ctx_overlap = 0.0
    if context:
        ctx_words = set(context.lower().split())
        for t in texts:
            t_words = set(t.lower().split())
            if ctx_words:
                ctx_overlap += len(ctx_words & t_words) / len(ctx_words)
        ctx_overlap /= max(n, 1)
    tbf = max(0.0, min(1.0, ctx_overlap))

    return {
        "cm": round(cm, 4),
        "da": round(da, 4),
        "drift": round(drift, 4),
        "dvg": round(dvg, 4),
        "int_val": round(int_val, 4),
        "tbf": round(tbf, 4),
    }


def check_directives(metrics: dict[str, float]) -> list[str]:
    fired = []
    for name, directive in DIRECTIVES.items():
        val = metrics.get(directive["metric"], 0)
        if directive["condition"] == "above" and val > directive["threshold"]:
            fired.append(name)
        elif directive["condition"] == "below" and val < directive["threshold"]:
            fired.append(name)
    return fired


def check_alerts(metrics: dict[str, float]) -> dict[str, list[str]]:
    """Return HIGH/LOW alert lists for metrics crossing the 0.80/0.20 thresholds."""
    high = [m for m in METRIC_NAMES if metrics.get(m, 0.0) >= ALERT_HIGH]
    low = [m for m in METRIC_NAMES if metrics.get(m, 0.0) <= ALERT_LOW]
    return {"HIGH": high, "LOW": low}


def delta_between(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    result = {}
    for m in METRIC_NAMES:
        result[f"delta_{m}"] = round((b.get(m, 0) - a.get(m, 0)), 4)
    return result
# ratios: loc_comments=65:33 imports_exports=2:4 calls_definitions=23:4
