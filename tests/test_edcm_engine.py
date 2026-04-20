import asyncio
from backend.edcm_engine import EDCMAnalyzer
from core.edcm import compute_metrics, check_alerts, check_directives


def _make_seeds(health_scores, masses=None, roles=None):
    if masses is None:
        masses = [1.0] * len(health_scores)
    if roles is None:
        roles = ["compute"] * len(health_scores)
    return [
        {"health_score": h, "mass": m, "role": r}
        for h, m, r in zip(health_scores, masses, roles)
    ]


def _analyze(seeds):
    return asyncio.run(EDCMAnalyzer().analyze(seeds))


# --- core/edcm.py unit tests ---

def test_compute_metrics_empty():
    m = compute_metrics([])
    assert set(m.keys()) == {"cm", "da", "drift", "dvg", "int_val", "tbf"}
    assert all(v == 0.0 for v in m.values())


def test_compute_metrics_single():
    m = compute_metrics([{"content": "hello world"}])
    assert all(0.0 <= v <= 1.0 for v in m.values())


def test_check_alerts_high():
    metrics = {"cm": 0.9, "da": 0.85, "drift": 0.1, "dvg": 0.1, "int_val": 0.5, "tbf": 0.5}
    alerts = check_alerts(metrics)
    assert "cm" in alerts["HIGH"]
    assert "da" in alerts["HIGH"]
    assert "drift" not in alerts["HIGH"]


def test_check_alerts_low():
    metrics = {"cm": 0.5, "da": 0.5, "drift": 0.5, "dvg": 0.5, "int_val": 0.1, "tbf": 0.1}
    alerts = check_alerts(metrics)
    assert "int_val" in alerts["LOW"]
    assert "tbf" in alerts["LOW"]
    assert "cm" not in alerts["LOW"]


def test_check_directives_fires():
    metrics = {"cm": 0.9, "da": 0.1, "drift": 0.1, "dvg": 0.1, "int_val": 0.5, "tbf": 0.5}
    fired = check_directives(metrics)
    assert "CONSTRAINT_REFOCUS" in fired


# --- EDCMAnalyzer unit tests ---

def test_analyze_healthy_system():
    result = _analyze(_make_seeds([0.9, 0.95, 0.88, 0.92]))
    assert result["artifact_type"] == "edcm_report"
    assert set(result["metrics"].keys()) == {"cm", "da", "drift", "dvg", "int_val", "tbf"}
    assert all(0.0 <= v <= 1.0 for v in result["metrics"].values())
    assert result["insights"]


def test_analyze_directives_high_cm():
    # mass=0, role=compute → expected_mass=4, total_mass=0 → cm=1.0 → CONSTRAINT_REFOCUS fires
    result = _analyze(_make_seeds([0.9, 0.9, 0.9, 0.9], masses=[0.0] * 4))
    assert "CONSTRAINT_REFOCUS" in result["directives"]
    assert result["monetization_value"] == "high"


def test_analyze_directives_low_int():
    # health_score=0.0 → int_val=0.0 <= 0.20 → INTENSITY_CALM fires
    result = _analyze(_make_seeds([0.0, 0.0, 0.0, 0.0], masses=[1.0] * 4))
    assert "INTENSITY_CALM" in result["directives"]


def test_analyze_no_false_directives_for_normal_system():
    # health=0.8 → cm~0, int_val=0.8, tbf~1.0 — no directives should fire
    result = _analyze(_make_seeds([0.8, 0.8, 0.8, 0.8], masses=[1.0] * 4))
    assert "CONSTRAINT_REFOCUS" not in result["directives"]
    assert "INTENSITY_CALM" not in result["directives"]
    assert "BALANCE_CONCISE" not in result["directives"]


def test_analyze_history_accumulates():
    analyzer = EDCMAnalyzer()
    seeds = _make_seeds([0.9, 0.9])
    asyncio.run(analyzer.analyze(seeds))
    asyncio.run(analyzer.analyze(seeds))
    summary = analyzer.get_artifact_summary()
    assert summary["total_artifacts"] == 2
