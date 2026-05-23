# CLAUDE.md — PCNA Codebase Guide

This file provides guidance to Claude Code and other AI assistants working in this repository.

---

## Project Overview

PCNA (Prime Circular Neural Architecture) is a deterministic, prime-indexed circular graph system for modular compute and real-time diagnostics. It has two distinct layers:

- **core/** — the inference engine: six rings of prime-indexed tensor nodes running heptagram propagation, coherence scoring, and EDCM diagnostics
- **backend/** — a FastAPI server that hosts seeds, integrates an LLM orchestrator, and exposes REST/WebSocket APIs

The canonical upstream is `The-Interdependency/a0`. Features are ported from there and adapted. Development happens on feature branches; PRs go to `main`.

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

Key: `_adj_distances(n)` uses `math.ceil(n/4)` to get gap=14 for n=53 (spec-correct). Keep `import math` — it is used here.

### `core/theta.py` — `ThetaTensor`
N=29 microkernel gate. Ragged circle counts per node (1–12), SHA-256 blueprint sharding, gate control via `GATE_THRESHOLD=0.45`. Not a PTCACore subclass — standalone. Neighbors hardcoded to `±1, ±7 mod 29`. Imported as `from .theta import ThetaTensor`.

### `core/sigma.py` — `SigmaRing` / `get_sigma()`
N=41 filesystem observer wrapping PTCACore. Tracks watched file mtimes, drains change events on `content_interval` cadence. Singleton via `get_sigma()`. In `core/pcna.py`, sigma import and use are wrapped in a broad `except Exception: pass` (silent). In `core/zeta.py`, the import is caught with `except ImportError` (silent return) and runtime errors with `except Exception` (logged). Treat sigma as optional — callers degrade gracefully if it raises.

### `core/memory_core.py` — `MemoryCore`
Parameterized long-term (N=19, seed=19) and short-term (N=17, seed=17) memory rings. Round-robin write, content-addressed query, `flush_to()` transfers short→long on positive reward.

### `core/pcna.py` — `PCNAEngine`
Six-ring inference engine. Key attributes: `self.phi`, `self.psi`, `self.omega`, `self.theta`, `self.memory_l`, `self.memory_s`. `RING_WEIGHTS` defines the **scored** ring set: `{phi, psi, omega, theta, memory_l, memory_s}`. `state()["rings"]` also includes `sigma` (optional observer, not scored). These two dicts are not required to be identical — only the scored rings need entries in `RING_WEIGHTS`. Checkpoints go in `.checkpoints/pcna_checkpoint.npz`.

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

**`RING_WEIGHTS` defines the scored ring set.** `RING_WEIGHTS` in `pcna.py` must match the keys used in `_coherence_score()` — currently `{phi, psi, omega, theta, memory_l, memory_s}`. `state()["rings"]` may include additional non-scored rings (currently `sigma`). If you add a scored ring, update both `RING_WEIGHTS` and `_coherence_score`. If you add a non-scored/observer ring, add it only to `state()["rings"]`.

**No `guardian` key anywhere.** The ring was renamed from `guardian` to `theta`. If you see `guardian` as a dict key or attribute (outside docstring prose), it is a bug.

**EDCM directive names are canonical.** Always `CONSTRAINT_REFOCUS`, `DISSONANCE_HALT`, `DRIFT_ANCHOR`, `DIVERGENCE_COMMIT`, `INTENSITY_CALM`, `BALANCE_CONCISE`. No internal abbreviations.

**`ALERT_HIGH` and `ALERT_LOW` before `DIRECTIVES`.** In `core/edcm.py`, constants must be defined before the `DIRECTIVES` dict that references them.

**No `pytest-asyncio`.** Tests use `asyncio.run()` directly. Do not add `@pytest.mark.asyncio`.

**No `sys.path.insert` in source files.** `conftest.py` handles the path. Do not add it to individual modules.

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

GitHub Actions runs a single `build` job on every push with two steps:

1. **flake8** — `--select=E9,F63,F7,F82` (syntax errors, undefined names). Must pass clean.
2. **pytest** — all `test_*.py` and `tests_*.py` in `tests/`. Must pass.

Common CI failures:
- Backslash-escaped triple quotes in f-strings → E999 SyntaxError
- Unused `global` declarations → F824
- Wrong import paths (e.g. `from src.core.*`) → ModuleNotFoundError
- Missing `asyncio.run()` / leftover `@pytest.mark.asyncio` decorator

---

## Adding a New Ring

1. Create `core/<name>.py` — implement the ring class with `tensor`, `ring_coherence`, `node_coherence`, `nudge()`, `state()` interface
2. Add it to `PCNAEngine.__init__()` as `self.<name>`
3. Add it to `state()["rings"]` under the same key
4. **If scored:** add weight to `RING_WEIGHTS` and key to `_coherence_score()`'s `ring_scores` dict
5. **If observer/optional:** skip `RING_WEIGHTS`; wrap access in `try/except` in `_inject()` and `reward()`
6. Add checkpoint save/load in `save_checkpoint()` / `load_checkpoint()` (scored rings only)

---

## Working with EDCM

`core/edcm.py` computes metrics from response text (content length, variance, context overlap). `backend/edcm_engine.py` computes metrics from seed state dicts (health scores, masses, roles). These are two separate derivation paths feeding the same six-family schema.

To add a new directive: add it to `DIRECTIVES` in `core/edcm.py`, add the corresponding firing condition to `EDCMAnalyzer._fire_directives()` in `backend/edcm_engine.py`, and add a test in `tests/test_edcm_engine.py`.

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
- `backend/server.py`: MongoDB connection failure is not handled gracefully; seed roles are hardcoded
- `requirements.txt`: missing `motor`, `python-dotenv`, `emergentintegrations`, `scipy`, `matplotlib`

---

## Frontend

React app in `frontend/`. Components: `TopologyVisualization`, `SystemHealthDashboard`, `EDCMArtifacts`, `LLMInterface`, `SMSConsole`. Not tested in CI. Backend served separately.

---

## Git Workflow

- Main branch: `main`
- Feature branches: `feat/<description>`, `fix/<description>`, `claude/update-from-interdependency-a0-*`
- Author: Erin Patrick Spencer
- License: Apache 2.0

## Agent module-build doctrine

Before adding a new module, route, service, adapter, schema, worker, engine,
UI panel, migration, or experiment, read:

`./.agents/skills/meta-module-build/SKILL.md`

New module work should start with a `MODULE_BUILD` block. Unknown fields must
be marked `hmmm`, not guessed.
