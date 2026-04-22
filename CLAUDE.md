# CLAUDE.md — PCNA Codebase Guide

## Project Overview

PCNA (Prime Circular Neural Architecture) is a deterministic, prime-indexed circular graph system for modular compute and real-time diagnostics. It has two distinct layers:

- **core/** — the inference engine: six rings of prime-indexed tensor nodes running heptagram propagation, coherence scoring, and EDCM diagnostics
- **backend/** — a FastAPI server that hosts seeds, integrates an LLM orchestrator, and exposes REST/WebSocket APIs

The canonical upstream is `The-Interdependency/a0`. Features are ported from there and adapted. Development happens on `claude/update-from-interdependency-a0-*` branches; PRs go to `main`.

---

## Repository Layout

```
core/           Engine modules (no FastAPI, no DB)
backend/        Server, LLM, optimization, SMS, Moltbook, outreach
frontend/src/   React dashboard (5 components)
tests/          pytest — no pytest-asyncio; use asyncio.run() for async tests
schemas/        JSON schemas
main.py         Seed runner entry point
conftest.py     sys.path insert — keeps pytest imports working
requirements.txt
```

---

## Core Modules — What Each Does

### `core/ptca_core.py` — `PTCACore`
Base class for all prime-ring tensors. Tensor shape: `[N, DIMS=4, PHASES=7, HEPT_SITES=7]`. Heptagram propagation via Euler steps (DT=0.01). Coherence = `1 - |ring - hub|_mean`. Used by Φ, Ψ, Ω, and Σ.

Key: `_adj_distances(n)` uses `math.ceil(n/4)` to get gap=14 for n=53 (spec-correct). Keep `import math` — it's used here.

### `core/theta.py` — `ThetaTensor`
N=29 microkernel gate. Ragged circle counts per node (1–12), SHA-256 blueprint sharding, gate control via `GATE_THRESHOLD=0.45`. Not a PTCACore subclass — standalone. Neighbors hardcoded to `±1, ±7 mod 29`. Imported as `from .theta import ThetaTensor`.

### `core/sigma.py` — `SigmaRing` / `get_sigma()`
N=41 filesystem observer wrapping PTCACore. Tracks watched file mtimes, drains change events on `content_interval` cadence. Singleton via `get_sigma()`. All callers in pcna.py and zeta.py use `try/except ImportError` — sigma is optional but present.

### `core/memory_core.py` — `MemoryCore`
Parameterized long-term (N=19, seed=19) and short-term (N=17, seed=17) memory rings. Round-robin write, content-addressed query, `flush_to()` transfers short→long on positive reward.

### `core/pcna.py` — `PCNAEngine`
Six-ring inference engine. Key attributes: `self.phi`, `self.psi`, `self.omega`, `self.theta`, `self.memory_l`, `self.memory_s`. `RING_WEIGHTS` dict uses keys matching `state()["rings"]` exactly: `phi, psi, omega, theta, memory_l, memory_s`. Checkpoints go in `.checkpoints/pcna_checkpoint.npz`.

### `core/edcm.py`
Six-family metrics (cm, da, drift, dvg, int_val, tbf) with `ALERT_HIGH=0.80`, `ALERT_LOW=0.20`. `DIRECTIVES` dict uses canonical names: `CONSTRAINT_REFOCUS`, `DISSONANCE_HALT`, `DRIFT_ANCHOR`, `DIVERGENCE_COMMIT`, `INTENSITY_CALM`, `BALANCE_CONCISE`. `check_directives()` returns a list of fired directive names.

### `core/zeta.py` — `ZetaEngine`
ZFAE: evaluates every assistant response via EDCM, nudges PCNAEngine.phi. Coherence formula: `cm*0.35 + da*0.25 + int_val*0.25 + (1-drift)*0.15`. Per-directory resolution (1–5) via prefix matching. Module-level singleton `_zeta_engine`. `_sigma_nudge_factors()` silently swallows `ImportError`; logs other exceptions.

### `core/merge.py` — `InstanceMerge`
Static methods: `absorb`, `fork`, `converge`. All output dicts use `theta_*` keys (not `guardian_*`). Federated averaging via `_fed_avg(a, b, alpha)`.

### `backend/edcm_engine.py` — `EDCMAnalyzer`
Derives EDCM metrics from `seed_states` dicts (require `health_score`, `mass`, `role` keys). Fires directives, generates insights/recommendations, assigns `monetization_value`. Async `analyze()` — call with `asyncio.run()` in tests.

---

## Key Invariants

**Ring weights and ring keys must match.** `RING_WEIGHTS` in `pcna.py` and `state()["rings"]` must have identical keys. Currently: `{phi, psi, omega, theta, memory_l, memory_s}`. If you add or rename a ring, update both.

**No `guardian` key anywhere.** The ring was renamed from `guardian` to `theta`. If you see `guardian` as a dict key or attribute (outside docstring prose), it's a bug.

**EDCM directive names are canonical.** Always `CONSTRAINT_REFOCUS`, `DISSONANCE_HALT`, `DRIFT_ANCHOR`, `DIVERGENCE_COMMIT`, `INTENSITY_CALM`, `BALANCE_CONCISE`. No internal abbreviations.

**`ALERT_HIGH` and `ALERT_LOW` before `DIRECTIVES`.** In `core/edcm.py`, constants must be defined before the `DIRECTIVES` dict that references them.

**No `pytest-asyncio`.** Tests use `asyncio.run()` directly. Do not add `@pytest.mark.asyncio`.

**No `sys.path.insert` in source files.** `conftest.py` handles the path. Don't add it to individual modules.

---

## Import Paths

Tests and backend modules import from the package root:
```python
from core.edcm import compute_metrics, check_alerts, check_directives
from backend.edcm_engine import EDCMAnalyzer
from core.pcna import PCNAEngine
```

The root `main.py` uses `from core.topology import ...` — correct.
`core/main.py` uses `from src.core.*` — broken, do not use.

---

## CI

GitHub Actions runs two jobs on every push:

1. **flake8** — `--select=E9,F63,F7,F82` (syntax errors, undefined names). Must pass clean.
2. **pytest** — all `test_*.py` and `tests_*.py` in `tests/`. Must pass.

Common CI failures seen:
- Backslash-escaped triple quotes in f-strings → E999 SyntaxError
- Unused `global` declarations → F824
- Wrong import paths (e.g. `from src.core.*`) → ModuleNotFoundError
- Missing `asyncio.run()` / leftover `@pytest.mark.asyncio` decorator

---

## Known Stubs (not yet implemented)

| File | What's missing |
|------|---------------|
| `core/routing_loop.py` | Only a print stub — `GlobalRouterZero` not implemented |
| `backend/moltbook_integration.py` | 100% mock data; all methods are TODOs |
| `backend/sms_service.py` | Twilio integration commented out; mock mode only |
| `backend/researcher_outreach.py` | `send_outreach()` is a stub; message generation works |

---

## Known Issues

- `core/memory_core.py`: `query()` is defined but never called anywhere
- `core/helix_vis.py`: saves to hardcoded `pcna_helix.gif`; no config
- `core/sigma.py`: `structural_interval` is stored but never acted on
- `core/merge.py`: `fork()` time-seeds its RNG — rapid calls may collide
- `backend/server.py`: MongoDB connection failure is not handled gracefully; seed roles are hardcoded in initialization (not topology-driven)
- `requirements.txt`: missing `motor`, `python-dotenv`, `emergentintegrations`, `scipy`, `matplotlib`

---

## Adding a New Ring

1. Create `core/<name>.py` — implement the ring class with `tensor`, `ring_coherence`, `node_coherence`, `nudge()`, `state()` interface
2. Add it to `PCNAEngine.__init__()` as `self.<name>`
3. Add the weight to `RING_WEIGHTS` in `core/pcna.py`
4. Add it to `state()["rings"]` with the same key as in `RING_WEIGHTS`
5. Add checkpoint save/load in `save_checkpoint()` / `load_checkpoint()`
6. Wire inject/reward as appropriate in `_inject()` and `reward()`

---

## Working with EDCM

`core/edcm.py` computes metrics from response text (content length, variance, context overlap). `backend/edcm_engine.py` computes metrics from seed state dicts (health scores, masses, roles). These are two separate derivation paths feeding the same six-family schema.

To add a new directive: add it to `DIRECTIVES` in `core/edcm.py`, add the corresponding firing condition to `EDCMAnalyzer._fire_directives()` in `backend/edcm_engine.py`, and add a test in `tests/test_edcm_engine.py`.

---

## Frontend

React app in `frontend/`. Components: `TopologyVisualization`, `SystemHealthDashboard`, `EDCMArtifacts`, `LLMInterface`, `SMSConsole`. Not tested in CI. Backend served separately.
