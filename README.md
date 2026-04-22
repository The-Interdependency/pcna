# PCNA — Prime Circular Neural Architecture

Deterministic, prime-indexed circular graph architecture for modular compute and real-time diagnostics.

---

## Architecture

PCNA organizes compute and diagnostics into **53 prime-indexed seeds** arranged on a unit-circle address space with heptagram (7-site) routing.

### Seed Topology

| Layer | Count | Role |
|-------|-------|------|
| Global router | 1 | Coordination root (ID 0) |
| Sentinels | 4 | Diagnostics — observe, do not compute |
| Meta routers | 7 | Cluster aggregation |
| Compute seeds | 49 (7×7) | Primary compute units |
| **Total** | **53** | Prime — avoids harmonic aliasing |

Each compute seed connects to heptagram neighbors (`±3 mod 7` within its meta cluster). Routing traverses the meta-router tree; sentinels scan with a 7:2 stride pattern and publish diagnostics only.

### Six-Ring Inference Engine (`core/pcna.py`)

The `PCNAEngine` runs a six-ring pipeline per inference call:

| Ring | Symbol | N | Seed | Role |
|------|--------|---|------|------|
| Phi | Φ | 53 | 53 | Cognitive substrate |
| Psi | Ψ | 53 | 43 | Self-model |
| Omega | Ω | 53 | 47 | Autonomy |
| Theta | Θ | 29 | — | Microkernel gate |
| Memory-L | — | 19 | 19 | Long-term memory |
| Memory-S | — | 17 | 17 | Short-term memory |
| Sigma | Σ | 41 | 41 | Filesystem observer |

**Ring weights** (coherence scoring): Φ 0.30 · Θ 0.20 · Ψ 0.15 · Ω 0.15 · Memory-L 0.12 · Memory-S 0.08

**Inference steps:**
1. **Project** — SHA-512(text) → 53-dim normalized signal
2. **Inject** — push signal into Φ; cross-inject Θ coherence → Φ, Φ coherence → Ψ, Σ coherence → Ψ, Memory-L hub → Ω
3. **Propagate** — heptagram propagation (Φ:10, Ψ:8, Ω:6, Θ:5 steps)
4. **PTCA-seed audit** — per-node hub-ring coherence for Φ/Ψ/Ω
5. **PCTA-circle audit** — gate status and circle counts on Θ
6. **Coherence score** — weighted ring coherence → winner ring + confidence

### EDCM — Six-Family Diagnostics

The EDCM subsystem (`core/edcm.py`, `backend/edcm_engine.py`) measures system health continuously:

| Metric | Key | Alert |
|--------|-----|-------|
| Constraint Mismatch | `cm` | HIGH ≥ 0.80 |
| Dissonance Accumulation | `da` | HIGH ≥ 0.80 |
| Drift | `drift` | HIGH ≥ 0.80 |
| Divergence | `dvg` | HIGH ≥ 0.80 |
| Intensity | `int_val` | LOW ≤ 0.20 |
| Turn-Balance Fairness | `tbf` | LOW ≤ 0.20 |

**Behavioral directives** fire automatically on threshold crossings:
`CONSTRAINT_REFOCUS` · `DISSONANCE_HALT` · `DRIFT_ANCHOR` · `DIVERGENCE_COMMIT` · `INTENSITY_CALM` · `BALANCE_CONCISE`

### ZetaEngine (`core/zeta.py`)

Non-LLM real-time learning: after every assistant response, ZFAE (Zeta Function Alpha Echo) computes EDCM coherence and drives PCNA Φ-ring reward backprop. Supports per-directory resolution levels (1–5).

---

## Repository Structure

```
pcna/
├── core/
│   ├── pcna.py           # PCNAEngine — six-ring inference pipeline
│   ├── ptca_core.py      # PTCACore — parameterized prime-ring tensor
│   ├── theta.py          # ThetaTensor — N=29 microkernel gate
│   ├── sigma.py          # SigmaRing — N=41 filesystem observer
│   ├── memory_core.py    # MemoryCore — long/short-term memory rings
│   ├── merge.py          # InstanceMerge — absorb/fork/converge
│   ├── zeta.py           # ZetaEngine — EDCM-driven backprop
│   ├── edcm.py           # EDCM metrics, alerts, directives
│   ├── topology.py       # PCNATopology — seed layout and routing
│   ├── tensor_engine.py  # TensorState, MarkovRecursion
│   ├── routing_loop.py   # GlobalRouterZero (stub — not implemented)
│   └── helix_vis.py      # Spectral helix visualizer
│
├── backend/
│   ├── server.py              # FastAPI — endpoints, WebSocket, MongoDB
│   ├── edcm_engine.py         # EDCMAnalyzer — artifacts and directives
│   ├── llm_abstraction.py     # LLMOrchestrator — multi-provider fallback
│   ├── optimization_engine.py # SelfOptimizer — health and anomaly monitor
│   ├── sms_service.py         # SMSService (Twilio stub)
│   ├── moltbook_integration.py # MoltbookClient (stub)
│   └── researcher_outreach.py # OutreachManager — researcher campaign
│
├── frontend/src/
│   ├── TopologyVisualization.js
│   ├── SystemHealthDashboard.js
│   ├── EDCMArtifacts.js
│   ├── LLMInterface.js
│   └── SMSConsole.js
│
├── tests/
│   ├── test_edcm_engine.py    # EDCM + EDCMAnalyzer unit tests
│   ├── test_tensor_engine.py  # MarkovRecursion mass-conservation tests
│   └── tests_topology.py     # PCNATopology routing tests
│
├── schemas/                   # JSON schema definitions
├── main.py                    # Seed runner entry point (FastAPI)
├── conftest.py                # sys.path setup for pytest
└── requirements.txt
```

---

## Installation

```bash
pip install -r requirements.txt
```

Additional dependencies required for full production use:

| Package | Required by |
|---------|-------------|
| `motor` | `backend/server.py` — async MongoDB |
| `python-dotenv` | environment variable loading |
| `emergentintegrations` | `backend/llm_abstraction.py` — multi-provider LLM |
| `scipy` | `proof_check.py` — spectral analysis |
| `matplotlib` | `core/helix_vis.py` — visualization |

---

## Running

### Seed runner (single node)

```bash
SEED_ID=1 ROLE=compute PORT=8001 python main.py
```

Multi-seed: set `SEED_URL_<id>=http://host:port` for each neighbor.

### Backend server

```bash
uvicorn backend.server:app --reload
```

### Tests

```bash
pytest
```

---

## Multi-Instance Mesh

`core/merge.py` provides three merge modes for running multiple `PCNAEngine` instances:

| Mode | Behaviour |
|------|-----------|
| `absorb(dominant, donor)` | Dominant absorbs donor state (α=0.15); donor retired |
| `fork(parent)` | Parent spawns child with copied state + Gaussian noise; both continue |
| `converge(a, b, alpha)` | Federated averaging in both directions (default α=0.50); both continue |

---

## Checkpointing

```python
engine = PCNAEngine()
engine.load_checkpoint()   # restore from .checkpoints/pcna_checkpoint.npz
# ... inference ...
engine.save_checkpoint()   # persist all ring tensors
```

---

## Design Principles

- **Deterministic routing** over opaque attention
- **Sparse communication** — bounded neighborhoods, heptagram adjacency
- **Explicit structure** — every ring self-declares identity in `state()`
- **Diagnostics first-class** — EDCM runs continuously, not as an afterthought
- **Inspectable** — checkpoint/restore, per-node coherence, per-ring state dicts
- **Modular growth** — rings are independently parameterized by `(n, seed, role)`

---

## Status

Experimental / research. Core inference engine and EDCM diagnostics are fully implemented. Several backend integrations are stubs awaiting external API credentials:

- **Twilio SMS** (`backend/sms_service.py`) — mock mode only
- **Moltbook** (`backend/moltbook_integration.py`) — all stubs
- **Researcher email sending** (`backend/researcher_outreach.py`) — generation implemented, sending is a stub
- **routing_loop.py** — not yet implemented
